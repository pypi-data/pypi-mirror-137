from db_hj3415 import mongo2
from scraper_hj3415.db_path import MONGO_ADDR

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

# 한개의 스파이더에서 연속 3일분량의 데이터가 전달된다.


class Mongo2Pipeline:
    client = mongo2.connect_mongo(MONGO_ADDR)

    # 몽고 데이터 베이스에 저장하는 파이프라인
    def process_item(self, item, spider):
        """
        아이템 구조
            title = scrapy.Field()
            date = scrapy.Field()
            value = scrapy.Field()
        """
        print(f"In the {self.__class__.__name__}...date : {item['date']} / title : {item['title']} / value : {item['value']}")
        mongo2.MI(self.client, item['title']).save(mi_dict={"date": item['date'], "value": item['value']})
        return item
