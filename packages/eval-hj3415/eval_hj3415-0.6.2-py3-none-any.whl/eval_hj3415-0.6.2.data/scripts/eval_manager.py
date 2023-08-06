import datetime
import os
import sys
import pprint
import pandas as pd
import argparse
from eval_hj3415 import eval, report
from util_hj3415 import noti
from db_hj3415 import dbpath, mongo2

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    present_addr = dbpath.load()
    client = mongo2.connect_mongo(present_addr)

    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser(
        prog="eval_manager",
        description="NFS eval program",
        epilog=f"Present addr - {present_addr}",
    )
    parser.add_argument('-m', '--message', action='store_true', help='Send report to telegram message.')

    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='valid subcommands',
        help='Additional help',
        dest="subcommand"
    )

    # create the parser for the "report" command
    report_parser = subparsers.add_parser(
        'report',
        description=f"Report nfs analysis",
        help=f"Report nfs analysis",
        epilog=f"Present addr - {present_addr}",
    )
    report_group = report_parser.add_mutually_exclusive_group()
    report_group.add_argument('-c', '--code', metavar='code', help='Report one code')
    report_group.add_argument('-a', '--all', action='store_true', help='Report all codes and save to database.')

    # create the parser for the "spac" command
    spac_parser = subparsers.add_parser(
        'spac',
        description=f"Find valuable spac",
        help=f"Find valuable spac",
        epilog=f"Present addr - {present_addr}",
    )

    # create the parser for the "db" command
    db_parser = subparsers.add_parser(
        'db',
        description=f"Help to set the mongo database address",
        help='Help to set the mongo database address',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{pprint.pformat(dbpath.make_path(('<ID>', '<PASS>')))}"
    )
    db_parser.add_argument('cmd', choices=['set', 'print'])
    db_parser.add_argument('-t', choices=['ATLAS', 'INNER', 'LOCAL', 'OUTER'])
    db_parser.add_argument('-i', help='Set id with address')
    db_parser.add_argument('-p', help='Set password with address')

    args = parser.parse_args()
    logger.debug(args)

    if args.subcommand == 'report':
        if args.code:
            print(report.for_console(client, args.code))
            if args.message:
                noti.telegram_to(botname='eval', text=report.for_telegram(client, args.code))
        elif args.all:
            df = eval.make_today_eval_df(present_addr)
            # pretty print df
            # https://www.delftstack.com/howto/python-pandas/how-to-pretty-print-an-entire-pandas-series-dataframe/
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            print(df)
            print("Save to mongo database...")
            mongo2.EvalWithDate(client, datetime.datetime.today().strftime('%Y%m%d'))

    elif args.subcommand == 'spac':
        for code, name, price in eval.yield_valid_spac(client):
            if args.message:
                noti.telegram_to(botname='eval',
                                 text=f'<<< code: {code} name: {name} price: {price} >>>')
        noti.telegram_to(botname='manager',
                         text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.subcommand}')
    elif args.subcommand == 'db':
        if args.cmd == 'print':
            print(present_addr)
        elif args.cmd == 'set':
            path = dbpath.make_path((args.i, args.p))[args.t]
            # print(path)
            # mongo2.connect_mongo(path)
            dbpath.save(path)
    else:
        parser.print_help()
        sys.exit()
