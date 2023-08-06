from datetime import datetime

from krx_hj3415 import krx
from db_hj3415 import mongo2
from scraper_hj3415.nfscrapy import scraper as scraper_nfs
from util_hj3415 import noti

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def make_refresh_targets(client) -> list:
    """
    1. krx 에서 10등분 종목코드를 받아 온다.\n(10일에 한번은 전체 코드를 리프레시 하는 의미)
    2. 리프레시 데이터베이스에서 리프레시 필요한 코드 리스트를 받는다.\n(분기, 반기, 사업보고서를 낸 종목을 정해진 횟수대로 리프레시 한다.)
    3. 합집합으로 1과 2를 합치고 리스트로 반환한다.
    """
    print('Union refreshing required codes with krx and dart...')

    # 1. krx에서 해당날짜 등분 종목코드를 받아온다.(28일 이후는 스크래핑을 생략한다.)
    pick_list_num = int(datetime.today().strftime('%d'))
    if pick_list_num > 28:
        krx_target_codes = []
    else:
        krx_target_codes = krx.make_parts(28)[pick_list_num-1]

    print(f'1. Get codes parts from krx (part num : {pick_list_num}): {len(krx_target_codes)}')
    logger.info(f'krx_parts_set : {krx_target_codes} {len(krx_target_codes)}')

    # 2. dart에서 저장한 리프레시 필요한 코드를 받아온다.
    SKIPPING_DAYS = 5  # 데이터베이스에 저장된 날짜에서 몇일이후부터 스크랩할 것인지..
    today = datetime.today()

    mongo_target_codes = []
    crefresh = mongo2.CRefresh(client, '005930')
    for code in crefresh.get_all_corps():
        crefresh.code = code
        date = crefresh.get_date()
        if date is None:
            continue
        elif (today - datetime.strptime(date, '%Y%m%d')).days >= SKIPPING_DAYS:
            # 데이터베이스의 날짜에서 SKIPPING_DAYS 일이 지난후 부터 카운터를 감소시킨다.
            if crefresh.count_down():
                mongo_target_codes.append(code)
    print(f'2. Making refresh target codes.. total {len(mongo_target_codes)} items..')
    logger.debug(f'mongo_target_codes : {mongo_target_codes} {len(mongo_target_codes)}')

    # 3. 합집합으로 1과 2를 합친다.
    rcodes = list(set(krx_target_codes) | set(mongo_target_codes))
    print(f'3. After union.. total {len(rcodes)} items..')

    logger.info(f'return value : {rcodes} {len(rcodes)}')
    return rcodes


def sync_mongo_with_krx(client):
    print('*' * 20, 'Sync with krx and mongodb', '*' * 20)
    corps_db = mongo2.Corps(client)
    all_codes_in_db = corps_db.get_all_corps()
    print('*' * 20, 'Refreshing krx.db...', '*' * 20)
    krx.make_db()
    print('*' * 80)
    all_codes_in_krx = krx.get_codes()
    print('\tThe number of codes in krx: ', len(all_codes_in_krx))
    logger.debug(all_codes_in_krx)
    try:
        print('\tThe number of dbs in mongo: ', len(all_codes_in_db))
        logger.debug(all_codes_in_db)
    except TypeError:
        err_msg = "Error while sync mongo data...it's possible mongo db doesn't set yet.."
        logger.error(err_msg)
        noti.telegram_to(botname='manager', text=err_msg)
        return
    del_targets = list(set(all_codes_in_db) - set(all_codes_in_krx))
    add_targets = list(set(all_codes_in_krx) - set(all_codes_in_db))
    print('\tDelete target: ', del_targets)
    print('\tAdd target: ', add_targets)

    for target in del_targets:
        corps_db.drop_db(target)
        print(f'\tDelete {target} db in mongo..')

    if len(add_targets) == 0:
        pass
    else:
        print(f'Starting.. c10346 scraper.. items : {len(add_targets)}')
        scraper_nfs.run('c103', add_targets)
        scraper_nfs.run('c104', add_targets)
        scraper_nfs.run('c106', add_targets)


def repair_db():
    """
    몽고 디비의 corps들의 integrity 검사후 이상시 재 스크래핑시도
    이상을 찾는 방법 - 각 컬렉션이 다 있는가. 각 컬렉션에서 연도와 분기의 도큐먼트 갯수가 같은가
    """
    pass
