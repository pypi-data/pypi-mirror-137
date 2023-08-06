# reference from https://livedata.tistory.com/27?category=1026425 (scrapy pipeline usage)
from . import items
from db_hj3415 import mongo2
from scraper_hj3415.db_path import MONGO_ADDR

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class C101Pipeline:
    client = mongo2.connect_mongo(MONGO_ADDR)
    # c101에서 eps, bps, per, pbr을 수동으로 계산하여 입력하는 파이프라인

    def process_item(self, item, spider):
        if isinstance(item, items.C101items):
            print(f"In the C101 pipeline...custom calculating EPS, BPS, PER, PBR")
            logger.debug('*** Start c101 pipeline ***')
            logger.debug(f"Raw data - EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
            # eps, bps, per, pbr을 직접 계산해서 바꾸기 위해 c104 page를 찾는다.
            try:
                logger.debug('Try to get c104 page for calculate values..')
                c104 = mongo2.C104(self.client, item['코드'], 'c104q')
                d, eps = c104.sum_recent_4q('EPS')    # 최근 4분기 eps값을 더한다.
                d, bps = c104.latest_value('BPS')     # 마지막 분기 bps값을 찾는다.

                # per, pbr을 구하는 람다함수
                cal_ratio = (lambda eps_bps, pprice:
                             None if eps_bps is None or eps_bps == 0 else round(int(pprice) / int(eps_bps), 2))
                cal_per = cal_ratio(eps, item['주가'])
                cal_pbr = cal_ratio(bps, item['주가'])
                logger.debug(f"After calc data - EPS:{eps} BPS:{bps} PER:{cal_per} PBR:{cal_pbr}")
                logger.debug(f"*** End c101 calculation pipeline {item['코드']} ***")
            except:
                logger.warning("Error on calculating custom EPS, BPS, PER, PBR, maybe DB hasn't c104q collection.")
                logger.warning(
                    f"We will use default scraped values -  EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
                return item
            item['EPS'], item['BPS'], item['PER'], item['PBR'] = eps, bps, cal_per, cal_pbr
        return item


class Mongo2Pipeline:
    client = mongo2.connect_mongo(MONGO_ADDR)

    # 몽고 데이터 베이스에 저장하는 파이프라인
    def process_item(self, item, spider):
        if isinstance(item, items.C101items):
            page = spider.name
            print(f"In the {self.__class__.__name__}...code : {item['코드']} / page : {spider.name}")
            r = mongo2.C101(self.client, item['코드']).save({
                "date": item['date'],
                "코드": item['코드'],
                "종목명": item['종목명'],
                "업종": item['업종'],
                "주가": item['주가'],
                "거래량": item['거래량'],
                "EPS": item['EPS'],
                "BPS": item['BPS'],
                "PER": item['PER'],
                "업종PER": item['업종PER'],
                "PBR": item['PBR'],
                "배당수익률": item['배당수익률'],
                "최고52주": item['최고52주'],
                "최저52주": item['최저52주'],
                "거래대금": item['거래대금'],
                "시가총액": item['시가총액'],
                "베타52주": item['베타52주'],
                "발행주식": item['발행주식'],
                "유통비율": item['유통비율'],
                "intro": item['intro1'] + item['intro2'] + item['intro3']
            })
        elif isinstance(item, items.C106items):
            page = ''.join(['c106', item['title']])
            print(f"In the {self.__class__.__name__}...code : {item['코드']} / page : {page}")
            logger.debug(item['df'].to_dict('records'))
            if page == 'c106y':
                r = mongo2.C106Y(self.client, item['코드']).save(item['df'])
            elif page == 'c106q':
                r = mongo2.C106Q(self.client, item['코드']).save(item['df'])
            else:
                raise
        elif isinstance(item, items.C108items):
            page = spider.name
            print(f"In the {self.__class__.__name__}...code : {item['코드']} / page : {spider.name}")
            logger.debug(item['df'].to_dict('records'))
            r = mongo2.C108(self.client, item['코드']).save(item['df'])
        elif isinstance(item, items.C103items):
            page = ''.join(['c103', item['title']])
            print(f"\tIn the {self.__class__.__name__}...code : {item['코드']} / page : {page}")
            logger.debug(item['df'].to_dict('records'))
            r = mongo2.C103(self.client, item['코드'], page).save(item['df'])
        elif isinstance(item, items.C104items):
            if item['title'].endswith('y'):
                page = 'c104y'
            elif item['title'].endswith('q'):
                page = 'c104q'
            else:
                raise ValueError
            print(f"In the {self.__class__.__name__}...code : {item['코드']} / page : {page}({item['title']})")
            logger.debug(item['df'].to_dict('records'))
            r = mongo2.C104(self.client, item['코드'], page).save(item['df'])
        else:
            raise
        if r:
            print(f"Save data to {page} collection {item['코드']} db successfully...")
        return item
