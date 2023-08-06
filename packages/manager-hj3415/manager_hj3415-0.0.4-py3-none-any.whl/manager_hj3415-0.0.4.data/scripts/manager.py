import os
import sys
import argparse
import pprint
import pandas as pd
import datetime

from krx_hj3415 import krx
from util_hj3415 import noti
from eval_hj3415 import report, eval
from manager_hj3415.manager import sync_mongo_with_krx, make_refresh_targets

from scraper_hj3415.miscrapy import scraper as scraper_mi
from scraper_hj3415.nfscrapy import scraper as scraper_nfs

from db_hj3415 import dbpath, mongo2


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


present_addr = dbpath.load()
client = mongo2.connect_mongo(present_addr)
spiders = ['c101', 'c106', 'c108', 'c103', 'c104']


def set_scraper_subcommand(parents_parser):
    """
    parents_parser - subparsers
    """
    scraper_cmd = spiders + ['mi', 'mi_hx', 'gm']
    # create the parser for the "scraper" command
    scraper_parser = parents_parser.add_parser(
        'scraper',
        description=f"Scraper nf, mi, gm",
        help='Scraper nf, mi, gm',
        epilog=f"Present addr - {present_addr}",
    )
    scraper_parser.add_argument('scraper_cmd', choices=scraper_cmd)
    scraper_parser.add_argument('-m', '--message', action='store_true', help='Send telegram message with result after work.')
    spiders_group = scraper_parser.add_mutually_exclusive_group()
    spiders_group.add_argument('-c', '--code', metavar='code', help='Scrape one code')
    spiders_group.add_argument('-a', '--all', action='store_true', help='Scrape all codes')


def set_refresh_subcommand(parents_parser):
    """
    parents_parser - subparsers
    """
    refresh_cmd = ['run', ]
    # create the parser for the "refresh" command
    refresh_parser = parents_parser.add_parser(
        'refresh',
        description=f"Refreshing codes periodically",
        help='Refreshing codes periodically',
        epilog=f"Present addr - {present_addr}",
    )
    refresh_parser.add_argument('refresh_cmd', choices=refresh_cmd)
    refresh_parser.add_argument('-m', '--message', action='store_true', help='Send telegram message with result after work.')


def set_eval_subcommand(parents_parser):
    """
    parents_parser - subparsers
    """
    eval_cmd = ['report', 'spac']
    # create the parser for the "eval" command
    eval_parser = parents_parser.add_parser(
        'eval',
        description=f"Evaluating and reporting",
        help='Evaluating and reporting',
        epilog=f"Present addr - {present_addr}",
    )
    eval_parser.add_argument('eval_cmd', choices=eval_cmd)
    eval_parser.add_argument('-m', '--message', action='store_true', help='Send telegram message with result after work.')
    spiders_group = eval_parser.add_mutually_exclusive_group()
    spiders_group.add_argument('-c', '--code', metavar='code', help='Scrape one code')
    spiders_group.add_argument('-a', '--all', action='store_true', help='Scrape all codes')


def set_db_subcommand(parents_parser):
    """
    parents_parser - subparsers
    """
    db_cmd = ['set', 'print', 'sync']
    # create the parser for the "db" command
    db_parser = parents_parser.add_parser(
        'db',
        description=f"Help to set the mongo database address",
        help='Help to set the mongo database address',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{pprint.pformat(dbpath.make_path(('<ID>', '<PASS>')))}"
    )
    db_parser.add_argument('db_cmd', choices=db_cmd)
    db_parser.add_argument('-m', '--message', action='store_true', help='Send telegram message with result after work.')
    db_parser.add_argument('-t', choices=['ATLAS', 'INNER', 'LOCAL', 'OUTER'])
    db_parser.add_argument('-i', help='Set id with address')
    db_parser.add_argument('-p', help='Set password with address')


def scraper_if_flow(iargs):
    if iargs.scraper_cmd in spiders:
        if iargs.code:
            scraper_nfs.run(iargs.scraper_cmd, [iargs.code, ])
            if iargs.message:
                noti.telegram_to('manager',
                                 f'>>> python {os.path.basename(os.path.realpath(__file__))} scraper {iargs.scraper_cmd} -c {iargs.code}')
        elif iargs.all:
            scraper_nfs.run(iargs.scraper_cmd, list(krx.get_codes()))
            if iargs.message:
                noti.telegram_to('manager',
                                 f'>>> python {os.path.basename(os.path.realpath(__file__))} scraper {iargs.scraper_cmd} -a')
        sys.exit()
    elif iargs.scraper_cmd == 'mi':
        if iargs.message:
            noti.telegram_to('manager',
                             f'>>> python {os.path.basename(os.path.realpath(__file__))} scraper {iargs.scraper_cmd}')
        scraper_mi.mi()
        sys.exit()
    elif iargs.scraper_cmd == 'mi_hx':
        if iargs.message:
            noti.telegram_to('manager',
                             f'>>> python {os.path.basename(os.path.realpath(__file__))} scraper {iargs.scraper_cmd}')
        scraper_mi.mihistory(year=1)
        sys.exit()
    elif iargs.scraper_cmd == 'gm':
        pass
        sys.exit()


def refresh_if_flow(iargs):
    if iargs.refresh_cmd == 'run':
        # 해당 날짜의 끝자리에 해당하는 220여개의 krx 코드 파트와 refresh db에 저장된 코드의 합집합으로 하여 매일 실행한다.
        refreshing_codes = make_refresh_targets(client)
        if iargs.message:
            noti.telegram_to(botname='manager',
                             text=f'Starting.. c10346 scraper.. items : {len(refreshing_codes)}')
        scraper_nfs.run('c103', refreshing_codes)
        scraper_nfs.run('c104', refreshing_codes)
        scraper_nfs.run('c106', refreshing_codes)
        if iargs.message:
            noti.telegram_to(botname='manager',
                             text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.cmd}')
        sys.exit()


def db_if_flow(iargs):
    if iargs.db_cmd == 'print':
        print(present_addr)
        sys.exit()
    elif iargs.db_cmd == 'sync':
        sync_mongo_with_krx(client)
        if iargs.message:
            noti.telegram_to(botname='manager',
                             text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.cmd}')
        sys.exit()
    elif iargs.db_cmd == 'set':
        path = dbpath.make_path((iargs.i, iargs.p))[iargs.t]
        # print(path)
        # mongo2.connect_mongo(path)
        dbpath.save(path)
        sys.exit()
        
        
def eval_if_flow(iargs):
    if iargs.eval_cmd == 'report':
        if iargs.code:
            print(report.for_console(client, iargs.code))
            if iargs.message:
                noti.telegram_to(botname='eval', text=report.for_telegram(client, iargs.code))
        elif iargs.all:
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

    elif iargs.eval_cmd == 'spac':
        for code, name, price in eval.yield_valid_spac(client):
            if iargs.message:
                noti.telegram_to(botname='eval',
                                 text=f'<<< code: {code} name: {name} price: {price} >>>')
        noti.telegram_to(botname='manager',
                         text=f'>>> python {os.path.basename(os.path.realpath(__file__))} {iargs.subcommand}')


if __name__ == '__main__':
    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser(
        prog="nfs_manager",
        description="My Scraper program",
        epilog=f"Present addr - {present_addr}",
    )

    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='valid subcommands',
        help='Additional help',
        dest="subcommand"
    )

    set_scraper_subcommand(subparsers)
    set_refresh_subcommand(subparsers)
    set_eval_subcommand(subparsers)
    set_db_subcommand(subparsers)

    args = parser.parse_args()
    logger.debug(args)

    if args.subcommand == 'scraper':
        # cmd - c101, c108, c103, c104, c106, mi, mi_hx, gm
        scraper_if_flow(args)
    elif args.subcommand == 'refresh':
        # cmd - run
        refresh_if_flow(args)
    elif args.subcommand == 'eval':
        # cmd - report, spac
        eval_if_flow(args)
    elif args.subcommand == 'db':
        # cmd - set, print, sync
        db_if_flow(args)
    else:
        parser.print_help()
        sys.exit()
