import os
import pickle
import pandas as pd
import argparse
import datetime
from eval_hj3415 import eval, report
from util_hj3415 import noti
from modules.db import DBPATH

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def make_pickle_for_django():
    # 장고에서 오늘 계산한 eval df를 복사해서 사용할수 있도록 피클로 만들어 저장한다.
    eval_path = os.path.join(DBPATH, 'eval.df')
    logger.info(eval_path)
    obj = datetime.datetime.now(), eval.make_today_eval_df()
    logger.info(obj)
    with open(eval_path, "wb") as fw:
        pickle.dump(obj, fw)
    

if __name__ == '__main__':
    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help=f"report, spac")

    code_group = parser.add_mutually_exclusive_group()
    code_group.add_argument('-c', '--code', metavar='code', help='Report one code')
    code_group.add_argument('-a', '--all', action='store_true', help='Report all codes')
    code_group.add_argument('-p', '--pickle', action='store_true', help='Make a pickle for using on django')
    parser.add_argument('-m', '--message', action='store_true', help='Send report to telegram message.')

    args = parser.parse_args()

    if args.cmd == 'report':
        if args.code:
            print(report.for_console(code=args.code))
            if args.message:
                noti.telegram_to(botname='eval', text=report.for_telegram(code=args.code))
        elif args.all:
            df = eval.make_today_eval_df()
            # pretty print df
            # https://www.delftstack.com/howto/python-pandas/how-to-pretty-print-an-entire-pandas-series-dataframe/
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            print(df)
        elif args.pickle:
            make_pickle_for_django()
            if args.message:
                noti.telegram_to(botname='manager',
                                 text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.cmd} -p')
    elif args.cmd == 'spac':
        for code, name, price in eval.yield_valid_spac():
            if args.message:
                noti.telegram_to(botname='eval',
                                 text=f'<<< code: {code} name: {name} price: {price} >>>')
        noti.telegram_to(botname='manager',
                         text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.cmd}')
    else:
        parser.print_help()
