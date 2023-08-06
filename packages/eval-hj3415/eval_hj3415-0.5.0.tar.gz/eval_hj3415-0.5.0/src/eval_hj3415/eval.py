"""red, mil, blue 3가지 분야에서 자료를 계산하여 리턴하는 함수 모음
"""
import math

from .db import CorpsEval
from db_hj3415 import mongo2
from util_hj3415 import utils
from krx_hj3415 import krx
import pandas as pd
import time
from multiprocessing import Process, cpu_count, Queue
import datetime

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

# 주식을 통한 기대수익률 - 금리가 3%일 경우 두배인 6% 정도로 잡는다.
EXPECT_EARN = 0.04


def red(client, code: str) -> dict:
    if utils.is_6digit(code):
        corps_eval = CorpsEval(client, code)
        c101 = mongo2.C101(client, code)
        c103 = mongo2.C103(client, code, 'c103재무상태표q')
    else:
        raise ValueError(f'Invalid code: {code}')

    d1, 지배주주당기순이익 = corps_eval.calc당기순이익()
    d2, 유동자산 = corps_eval.calc유동자산()
    d3, 유동부채 = corps_eval.calc유동부채()
    d4, 부채평가 = corps_eval.calc비유동부채()

    c103.page = 'c103재무상태표q'
    d5, 투자자산 = c103.latest_value('투자자산')
    d6, 투자부동산 = c103.latest_value('투자부동산')

    # 사업가치 계산 - 지배주주지분 당기순이익 / 기대수익률
    사업가치 = round(지배주주당기순이익 / EXPECT_EARN, 2)

    # 재산가치 계산 - 유동자산 - (유동부채*1.2) + 고정자산중 투자자산
    재산가치 = round(유동자산 - (유동부채 * 1.2) + 투자자산 + 투자부동산, 2)

    발행주식수 = c103.latest_value('발행주식수')[1]
    if math.isnan(발행주식수):
        rc101 = c101.get_recent()
        logger.error(rc101)
        발행주식수 = utils.to_int(rc101.get('발행주식'))
    else:
        발행주식수 = 발행주식수 * 1000

    try:
        red_price = round(((사업가치 + 재산가치 - 부채평가) * 100000000) / 발행주식수)
    except (ZeroDivisionError, ValueError) as e:
        logger.error(f'{e} : {code}')
        red_price = float('nan')

    logger.debug(f'Red Price : {red_price}원')
    return {
        'red_price': red_price,
        '사업가치': 사업가치,
        '재산가치': 재산가치,
        '부채평가': 부채평가,
        '발행주식수': 발행주식수,
        'date': [i for i in {d1, d2, d3, d4, d5, d6} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def mil(client, code: str) -> dict:
    if utils.is_6digit(code):
        corps_eval = CorpsEval(client, code)
        c103 = mongo2.C103(client, code, 'c103현금흐름표q')
        c104 = mongo2.C104(client, code, 'c104q')
    else:
        raise ValueError(f'Invalid code: {code}')

    marketcap = corps_eval.marketcap
    logger.info(f'{code} market cap: {marketcap}')
    fcf_dict = corps_eval.findFCF()
    pfcf_dict = corps_eval.findPFCF()
    d1, 지배주주당기순이익 = corps_eval.calc당기순이익()

    d2, 재무활동현금흐름 = c103.sum_recent_4q(title='재무활동으로인한현금흐름')
    d3, 영업활동현금흐름 = c103.sum_recent_4q(title='영업활동으로인한현금흐름')

    d4, roic = c104.sum_recent_4q('ROIC')
    d5, roe = c104.latest_value('ROE')
    pcr_dict = c104.find('PCR')

    주주수익률 = float('nan') if marketcap == 0 else round((재무활동현금흐름 / marketcap * -100), 2)
    이익지표 = float('nan') if marketcap == 0 else round((지배주주당기순이익 - 영업활동현금흐름) / marketcap, 5)

    logger.info(f'{code} fcf_dict : {fcf_dict}')
    logger.info(f"{code} market_cap : {marketcap}")
    logger.info(f'{code} pfcf_dict : {pfcf_dict}')
    logger.info(f'{code} pcr_dict : {pcr_dict}')

    return {
        '주주수익률': 주주수익률,
        '이익지표': 이익지표,
        '투자수익률': {'ROIC': roic, 'ROE': roe},
        '가치지표': {'FCF': fcf_dict, 'PFCF': pfcf_dict, 'PCR': pcr_dict},
        'date': [i for i in {d1, d2, d3, d4, d5} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def blue(client, code: str) -> dict:
    """
    <유동비율>
    100미만이면 주의하나 현금흐름창출력이 좋으면 괜찮을수 있다.
    만약 100%이하면 유동자산에 추정영업현금흐름을 더해서 다시계산해보아 기회를 준다.
    <이자보상배율>
    이자보상배율 영업이익/이자비용으로 1이면 자금사정빡빡 5이상이면 양호
    <순운전자금회전율>
    순운전자금 => 기업활동을 하기 위해 필요한 자금 (매출채권 + 재고자산 - 매입채무)
    순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
    <재고자산회전율>
    재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
    재고자산회전율이 작아지면 재고가 쌓인다는뜻
    <순부채비율>
    부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
    순부채 비율이 30%이상이면 좋치 않다.
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """

    if utils.is_6digit(code):
        corps_eval = CorpsEval(client, code)
        c104 = mongo2.C104(client, code, 'c104y')
    else:
        raise ValueError(f'Invalid code: {code}')

    ###############################################################

    d1, 유동비율 = corps_eval.calc유동비율(nan_to_zero=False)
    logger.info(f'유동비율 {유동비율}/{d1}')

    ###############################################################

    dict이자보상배율 = c104.find('이자보상배율')
    dict순운전자본회전율 = c104.find('순운전자본회전율')
    dict재고자산회전율 = c104.find('재고자산회전율')
    dict순부채비율 = c104.find('순부채비율')

    c104.page = 'c104q'
    d2, 이자보상배율 = c104.latest_value('이자보상배율')
    d3, 순운전자본회전율 = c104.latest_value('순운전자본회전율')
    d4, 재고자산회전율 = c104.latest_value('재고자산회전율')
    d5, 순부채비율 = c104.latest_value('순부채비율')

    logger.info(f'이자보상배율 : {이자보상배율} {dict이자보상배율}')
    logger.info(f'순운전자본회전율 : {순운전자본회전율} {dict순운전자본회전율}')
    logger.info(f'재고자산회전율 : {재고자산회전율} {dict재고자산회전율}')
    logger.info(f'순부채비율 : {순부채비율} {dict순부채비율}')

    ################################################################

    return {
        '유동비율': 유동비율,
        '이자보상배율': (이자보상배율, dict이자보상배율),
        '순운전자본회전율': (순운전자본회전율, dict순운전자본회전율),
        '재고자산회전율': (재고자산회전율, dict재고자산회전율),
        '순부채비율': (순부채비율, dict순부채비율),
        'date': [i for i in {d1, d2, d3, d4, d5} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def growth(client, code: str) -> dict:
    """
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """
    if utils.is_6digit(code):
        c104 = mongo2.C104(client, code, 'c104y')
        c106y = mongo2.C106Y(client, code)
    else:
        raise ValueError(f'Invalid code: {code}')

    dict매출액증가율 = c104.find('매출액증가율')

    c104.page = 'c104q'
    d1, 매출액증가율 = c104.latest_value('매출액증가율')

    logger.info(f'매출액증가율 : {매출액증가율} {dict매출액증가율}')

    ################################################################

    # c106 에서 타 기업과 영업이익률 비교
    try:
        dict영업이익률 = c106y.find('영업이익률')
    except KeyError:
        dict영업이익률 = {'Unnamed': float('nan')}
    logger.info(f'{code} 영업이익률 {dict영업이익률}')

    return {
        '매출액증가율': (매출액증가율, dict매출액증가율),
        '영업이익률': dict영업이익률,
        'date': [d1, ]}


"""
- 각분기의 합이 연이 아닌 타이틀(즉 sum_4q를 사용하면 안됨)
'*(지배)당기순이익'
'*(비지배)당기순이익'
'장기차입금'
'현금및예치금'
'매도가능금융자산'
'매도파생결합증권'
'만기보유금융자산'
'당기손익-공정가치측정금융부채'
'당기손익인식(지정)금융부채'
'단기매매금융자산'
'단기매매금융부채'
'예수부채'
'차입부채'
'기타부채'
'보험계약부채(책임준비금)'
'*CAPEX'
'ROE'
"""

"""
- sum_4q를 사용해도 되는 타이틀
'자산총계'
'당기순이익'
'유동자산'
'유동부채'
'비유동부채'

'영업활동으로인한현금흐름'
'재무활동으로인한현금흐름'
'ROIC'
"""


def _make_df_part(client, codes: list, q):
    def make_record(c: str) -> dict:
        # 장고에서 사용할 eval 테이블을 만들기 위해 각각의 레코드를 구성하는 함수
        c101 = mongo2.C101(client, c).get_recent()

        red_dict = red(client, c)
        mil_dict = mil(client, c)
        growth_dict = growth(client, c)

        mil_date = mil_dict['date']
        red_date = red_dict['date']
        growth_date = growth_dict['date']

        return {
            'code': c101['코드'],
            '종목명': c101['종목명'],
            '주가': utils.to_int(c101['주가']),
            'PER': utils.to_float(c101['PER']),
            'PBR': utils.to_float(c101['PBR']),
            '시가총액': utils.to_float(c101['시가총액']),
            'RED': utils.to_int(red_dict['red_price']),
            '주주수익률': utils.to_float(mil_dict['주주수익률']),
            '이익지표': utils.to_float(mil_dict['이익지표']),
            'ROIC': utils.to_float(mil_dict['투자수익률']['ROIC']),
            'ROE': utils.to_float(mil_dict['투자수익률']['ROE']),
            'PFCF': utils.to_float(CorpsEval.get_recent(mil_dict['가치지표']['PFCF'])[1]),
            'PCR': utils.to_float(CorpsEval.get_recent(mil_dict['가치지표']['PCR'])[1]),
            '매출액증가율': utils.to_float(growth_dict['매출액증가율'][0]),
            'date': list(set(mil_date + red_date + growth_date))
        }

    t = len(codes)
    d = []
    for i, code in enumerate(codes):
        print(f'{i+1}/{t} {code}')
        try:
            d.append(make_record(code))
        except:
            logger.error(f'error on {code}')
            continue
    df = pd.DataFrame(d)
    logger.info(df)
    q.put(df)


def make_today_eval_df(db_addr: str, refresh: bool = False) -> pd.DataFrame:
    """ 멀티프로세싱을 사용하여 전체 종목의 eval 을 데이터프레임으로 만들어 반환

    기본값으로 refresh 는 False 로 설정되어 당일자의 저장된 데이터프레임이 있으면 새로 생성하지 않고 mongo DB를 이용한다.
    """
    def _code_divider(entire_codes: list) -> tuple:
        # 전체 종목코드를 리스트로 넣으면 cpu 코어에 맞춰 나눠준다.
        # https://stackoverflow.com/questions/19086106/how-to-utilize-all-cores-with-python-multiprocessing
        def _split_list(alist, wanted_parts=1):
            # 멀티프로세싱할 갯수로 리스트를 나눈다.
            # https://www.it-swarm.dev/ko/python/%EB%8D%94-%EC%9E%91%EC%9D%80-%EB%AA%A9%EB%A1%9D%EC%9C%BC%EB%A1%9C-%EB%B6%84%ED%95%A0-%EB%B0%98%EC%9C%BC%EB%A1%9C-%EB%B6%84%ED%95%A0/957910776/
            length = len(alist)
            return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                    for i in range(wanted_parts)]

        core = cpu_count()
        print(f'Get number of core for multiprocessing : {core}')
        n = core - 1
        if len(entire_codes) < n:
            n = len(entire_codes)
        print(f'Split total {len(entire_codes)} codes by {n} parts ...')
        divided_list = _split_list(entire_codes, wanted_parts=n)
        return n, divided_list

    today_str = datetime.datetime.today().strftime('%Y%m%d')
    client = mongo2.connect_mongo(db_addr)
    df = mongo2.EvalWithDate(client, today_str).load_df()
    if refresh or len(df) == 0:
        codes = mongo2.Corps(client).get_all_corps()

        print('*' * 25, f"Eval all using multiprocess", '*' * 25)
        print(f'Total {len(codes)} items..')
        logger.info(codes)
        n, divided_list = _code_divider(codes)

        start_time = time.time()
        q = Queue()
        ths = []
        for i in range(n):
            ths.append(Process(target=_make_df_part, args=(client, divided_list[i], q)))
        for i in range(n):
            ths[i].start()
        df_list = []
        for i in range(n):
            df_list.append(q.get())
        # 부분데이터프레임들을 하나로 합침
        final_df = pd.concat(df_list, ignore_index=True)
        for i in range(n):
            ths[i].join()
        print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')
        logger.debug(final_df)
        print(f"Save to mongo db(db: eval col: {today_str}")
        mongo2.EvalWithDate(client, today_str).save_df(final_df)
    else:
        print(f"Use saved dataframe from mongo db..")
        final_df = mongo2.EvalWithDate(client, today_str).load_df()
    return final_df


def yield_valid_spac(client) -> tuple:
    """
    전체 스팩주의 현재가를 평가하여 2000원 이하인 경우 yield한다.

    Returns:
        tuple: (code, name, price)
    """
    codes = mongo2.Corps(client).get_all_corps()
    logger.info(f'len(codes) : {len(codes)}')
    print('<<< Finding valuable SPAC >>>')
    for i, code in enumerate(codes):
        name = krx.get_name(code)
        logger.info(f'code : {code} name : {name}')
        if '스팩' in str(name):
            logger.info(f'>>> spac - code : {code} name : {name}')
            price, _, _ = utils.get_price_now(code=code)
            if price <= 2000:
                logger.warning(f'현재가:{price}')
                print(f"code: {code} name: {name}, price: {price}")
                yield code, name, price
