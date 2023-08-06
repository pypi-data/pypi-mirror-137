import math
from db_hj3415 import mongo2
from typing import Tuple, List
from util_hj3415 import utils
from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


class CorpsEval:
    """eval에서 사용되는 여러가지 지수를 계산하는 함수 모음.

    """

    def __init__(self,client, code: str):
        if utils.is_6digit(code):
            self.client = client
            self.code = code
            self.c101 = mongo2.C101(self.client, code)
            self.c103 = mongo2.C103(self.client, code, 'c103재무상태표y')
            self.c104 = mongo2.C104(self.client, code, 'c104y')
        else:
            raise ValueError(f'Invalid code : {code}')
        # C103이 억단위로 계산되기 때문에 시가총액도 억단위로 맞춘다.
        try:
            self.marketcap = int(self.c101.get_recent()['시가총액']) / 100000000
        except KeyError:
            self.marketcap = float('nan')

    def chg_code(self, code: str):
        if utils.is_6digit(code):
            self.code = code
            self.c101.code = code
            self.c103.code = code
            self.c104.code = code
        else:
            raise ValueError(f'Invalid code : {code}')
        # C103이 억단위로 계산되기 때문에 시가총액도 억단위로 맞춘다.
        try:
            self.marketcap = int(self.c101.get_recent()['시가총액']) / 100000000
        except KeyError:
            self.marketcap = float('nan')

    @staticmethod
    def sum_except_nan(targets: List[Tuple[str, float]]) -> Tuple[str, float]:
        """

        (date, value) 에서 value 가 nan 인 경우 해당 튜플을 건너뛰고 아닌 경우에만 합을 계산하여 구하는 함수

        Args:
            targets (List): (date, value) 형식의 튜플을 원소로 가지는 리스트

        Returns:
            Tuple: (date, 총합 value) 형식의 튜플
        """
        logger.info(f'sum_except_nan : {targets}')
        s_date = set()
        t_value = 0
        for date, value in targets:
            s_date.add(date)
            t_value += value
        try:
            return list(s_date)[0], round(t_value, 2)
        except IndexError:
            # s_date의 값이 하나도 없는 경우
            return '', 0

    def calc당기순이익(self) -> Tuple[str, float]:
        """지배지분 당기순이익 계산

        일반적인 경우로는 직전 지배주주지분 당기순이익을 찾아서 반환한다.\n
        금융기관의 경우는 지배당기순이익이 없기 때문에\n
        계산을 통해서 간접적으로 구한다.\n
        """
        self.c103.page = 'c103재무상태표q'
        profit_dict = self.c103.find(title='*(지배)당기순이익')
        logger.info(f'*(지배)당기순이익 : {profit_dict}')
        if len(profit_dict) == 0:
            # 금융관련은 재무상태표에 지배당기순이익이 없어서 손익계산서의 당기순이익에서 비지배당기순이익을 빼서 간접적으로 구한다.
            self.c103.page = 'c103손익계산서q'
            t1 = self.c103.sum_recent_4q('당기순이익')
            logger.info(f'당기순이익(손익계산서) : {t1[0]}\t{t1[1]}')
            self.c103.page = 'c103재무상태표q'
            t2 = self.c103.latest_value('*(비지배)당기순이익')
            logger.info(f'*(비지배)당기순이익 : {t2[0]}\t{t2[1]}')
            return self.sum_except_nan([t1, t2])
        else:
            return self.c103.latest_value('*(지배)당기순이익')

    def calc유동자산(self) -> Tuple[str, float]:
        """유효한 유동자산 계산

        일반적인 경우로 유동자산을 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        Red와 Blue에서 사용한다.\n
        """
        self.c103.page = 'c103재무상태표q'
        asset_dict = self.c103.find(title='유동자산')
        logger.info(f'유동자산 : {asset_dict}')
        if len(asset_dict) == 0:
            # 금융관련업종...
            t1 = self.c103.latest_value('현금및예치금')
            logger.info(f'현금및예치금 : {t1[0]}\t{t1[1]}')
            t2 = self.c103.latest_value('단기매매금융자산')
            logger.info(f'단기매매금융자산 : {t2[0]}\t{t2[1]}')
            t3 = self.c103.latest_value('매도가능금융자산')
            logger.info(f'매도가능금융자산 : {t3[0]}\t{t3[1]}')
            t4 = self.c103.latest_value('만기보유금융자산')
            logger.info(f'만기보유금융자산 : {t4[0]}\t{t4[1]}')
            return self.sum_except_nan([t1, t2, t3, t4])
        else:
            return self.c103.sum_recent_4q('유동자산')

    def calc유동부채(self) -> Tuple[str, float]:
        """유효한 유동부채 계산

        일반적인 경우로 유동부채를 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        Red와 Blue에서 사용한다.\n
        """
        self.c103.page = 'c103재무상태표q'
        debt_dict = self.c103.find(title='유동부채')
        logger.info(f'유동부채 : {debt_dict}')
        if len(debt_dict) == 0:
            # 금융관련업종...
            t1 = self.c103.latest_value('당기손익인식(지정)금융부채')
            logger.info(f'당기손익인식(지정)금융부채 : {t1[0]}\t{t1[1]}')
            t2 = self.c103.latest_value('당기손익-공정가치측정금융부채')
            logger.info(f'당기손익-공정가치측정금융부채 : {t2[0]}\t{t2[1]}')
            t3 = self.c103.latest_value('매도파생결합증권')
            logger.info(f'매도파생결합증권 : {t3[0]}\t{t3[1]}')
            t4 = self.c103.latest_value('단기매매금융부채')
            logger.info(f'단기매매금융부채 : {t4[0]}\t{t4[1]}')
            return self.sum_except_nan([t1, t2, t3, t4])
        else:
            return self.c103.sum_recent_4q('유동부채')

    def calc비유동부채(self) -> Tuple[str, float]:
        """유효한 비유동부채 계산

        일반적인 경우로 비유동부채를 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        Red와 Blue에서 사용한다.\n
        """
        self.c103.page = 'c103재무상태표q'
        debt_dict = self.c103.find(title='비유동부채')
        logger.info(f'유동부채 : {debt_dict}')
        if len(debt_dict) == 0:
            # 금융관련업종...
            # 보험관련업종은 예수부채가 없는대신 보험계약부채가 있다...
            t1 = self.c103.latest_value('예수부채')
            logger.info(f'예수부채 : {t1[0]}\t{t1[1]}')
            t2 = self.c103.latest_value('보험계약부채(책임준비금)')
            logger.info(f'보험계약부채(책임준비금) : {t2[0]}\t{t2[1]}')
            t3 = self.c103.latest_value('차입부채')
            logger.info(f'차입부채 : {t3[0]}\t{t3[1]}')
            t4 = self.c103.latest_value('기타부채')
            logger.info(f'기타부채 : {t4[0]}\t{t4[1]}')
            return self.sum_except_nan([t1, t2, t3, t4])
        else:
            return self.c103.sum_recent_4q('비유동부채')

    def calc유동비율(self, nan_to_zero: bool = True) -> Tuple[str, float]:
        """유동비율계산 - Blue에서 사용

        c104q에서 최근유동비율 찾아보고 유효하지 않거나 \n
        100이하인 경우에는수동으로 계산해서 다시 한번 평가해 본다.\n
        """
        self.c104.page = 'c104q'
        d1, 유동비율 = self.c104.latest_value('유동비율')
        logger.info(f'{self.code} 유동비율 : {유동비율}')

        if math.isnan(유동비율) or 유동비율 < 100:
            logger.warning('유동비율 is under 100 or nan..so we will recalculate..')
            d1, 유동자산 = self.calc유동자산()
            d2, 유동부채 = self.calc유동부채()

            self.c103.page = 'c103현금흐름표q'
            d3, 추정영업현금흐름 = self.c103.sum_recent_4q('영업활동으로인한현금흐름')

            try:
                logger.info(f'{self.code} 계산전 유동비율 : {유동비율}')
                계산된유동비율 = round(((유동자산 + 추정영업현금흐름) / 유동부채) * 100, 2)
                logger.info(f'{self.code} 계산된 유동비율 : {계산된유동비율}')
                return list({d1, d2, d3})[0], 계산된유동비율
            except ZeroDivisionError:
                if nan_to_zero:
                    return list({d1, d2, d3})[0], 0
                else:
                    return list({d1, d2, d3})[0], float('nan')
        else:
            return d1, 유동비율

    def findFCF(self) -> dict:
        """FCF 계산

        FCF = 영업활동현금흐름 - CAPEX\n
        영업활동현금흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 딕셔너리로 반환한다.\n

        Returns:
            dict: 계산된 fcf 딕셔너리 또는 영업현금흐름 없는 경우 - {}

        Note:
            CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.\n

        """
        self.c103.page = 'c103현금흐름표y'
        영업활동으로인한현금흐름 = self.c103.find(title='영업활동으로인한현금흐름')
        self.c103.page = 'c103재무상태표y'
        capex = self.c103.find(title='*CAPEX')

        logger.debug(f'영업활동으로인한현금흐름 {영업활동으로인한현금흐름}')
        logger.debug(f'CAPEX {capex}')

        if len(영업활동으로인한현금흐름) == 0:
            return {}

        if len(capex) == 0:
            # CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.
            return 영업활동으로인한현금흐름

        # 영업 활동으로 인한 현금 흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 리턴값으로 fcf 딕셔너리를 반환한다.
        r_dict = {}
        for i in range(len(영업활동으로인한현금흐름)):
            # 영업활동현금흐름에서 아이템을 하나씩 꺼내서 CAPEX 전체와 비교하여 같으면 차를 구해서 r_dict 에 추가한다.
            date_cashflow, value_cashflow = 영업활동으로인한현금흐름.popitem()
            # 해당 연도의 capex 가 없는 경우도 있어 일단 capex를 0으로 치고 먼저 추가한다.
            r_dict[date_cashflow] = value_cashflow
            for date_capex, value_capex in capex.items():
                if date_cashflow == date_capex:
                    r_dict[date_cashflow] = round(value_cashflow - value_capex, 2)
        logger.debug(f'r_dict {r_dict}')
        # 연도순으로 정렬해서 딕셔너리로 반환한다.
        return dict(sorted(r_dict.items(), reverse=False))

    def findPFCF(self) -> dict:
        """Price to Free Cash Flow Ratio 계산

        PFCF = 시가총액 / FCF

        Note:
            https://www.investopedia.com/terms/p/pricetofreecashflow.asp
        """
        fcf_dict = self.findFCF()
        logger.debug(f'fcf_dict : {fcf_dict}')
        pfcf_dict = {}
        for date, fcf_one in fcf_dict.items():
            if fcf_one == 0:
                continue
            else:
                pfcf_dict[date] = round(self.marketcap / fcf_one, 2)
        logger.debug(f'pfcf_dict : {pfcf_dict}')
        return pfcf_dict

    @staticmethod
    def get_recent(data: dict, nan_to_zero: bool = False) -> Tuple[str, float]:
        """연/분기 딕셔너리에서 최근 자료를 추출해 반환함.

        최근 자료를 일차로 추출해서 nan 이면 한번 더 그 이전 자료를 추출해서 반환한다.

        Args:
             data(dict): 연/분기 재무재표 딕셔너리 자료
             nan_to_zero (bool): 각 함수에서 반환하는 값이 nan 일 경우 0으로 치환할지 여부 결정
        """
        # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
        # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
        od = OrderedDict(sorted(data.items(), reverse=False))
        logger.info(f'{od}')
        try:
            last_one = od.popitem(last=True)
        except KeyError:
            # when dictionary is empty
            if nan_to_zero:
                return '', 0
            else:
                return '', float('nan')

        logger.info(f'last_one : {last_one}')
        if isinstance(last_one[1], str):
            # last_one : ('Unnamed: 1', '데이터가 없습니다.') 인 경우
            if nan_to_zero:
                return '', 0
            else:
                return '', float('nan')
        elif math.isnan(last_one[1]):
            try:
                last_one = od.popitem(last=True)
            except KeyError:
                # when dictionary is empty
                if nan_to_zero:
                    return '', 0
                else:
                    return '', float('nan')
        if nan_to_zero:
            return last_one[0], 0 if math.isnan(last_one[1]) else last_one[1]
        else:
            return tuple(last_one)
