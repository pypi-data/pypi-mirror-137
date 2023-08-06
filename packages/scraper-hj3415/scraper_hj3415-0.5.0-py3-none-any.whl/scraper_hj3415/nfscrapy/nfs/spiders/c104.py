import time
import scrapy
from util_hj3415 import utils
from scrapy.selector import Selector
from abc import *

from nfs import items
from nfs.spiders import common

# cmd usage : scrapy crawl c104_aq -a code=005930


class C104Spider(scrapy.Spider, metaclass=ABCMeta):
    name = 'c104'
    allowed_domains = ['navercomp.wisereport.co.kr']
    WAIT = 1.5

    def __init__(self, code, title):
        super(C104Spider, self).__init__()
        self.codes = common.adjust_arg_type(code)
        self.driver = utils.get_driver()
        self.title = title  # ex- 수익성q

    def start_requests(self):
        # reference from https://docs.scrapy.org/en/latest/topics/request-response.html
        total_count = len(self.codes)
        print(f'Start scraping {self.name}, {total_count} codes...')
        self.logger.info(f'entire codes list - {self.codes}')

        # 실제로 페이지를 스크랩하기위해 호출
        for i, one_code in enumerate(self.codes):
            print(f'{i + 1}/{total_count}. Parsing {self.title}...{one_code}')
            yield scrapy.Request(
                url=f'https://navercomp.wisereport.co.kr/v2/company/c1040001.aspx?cmp_cd={one_code}',
                callback=getattr(self, f'parse_c104'),
                cb_kwargs=dict(code=one_code)
            )

    def parse_c104(self, response, code):
        # 페이지를 먼저 한번 호출하여 버튼을 눌러 세팅한다.
        self.setting_page(response.url)

        # html에서 table을 추출하여 dataframe생성
        self.driver.get(response.url)
        time.sleep(self.WAIT)
        html = Selector(text=self.driver.page_source)
        table_xpath = '//table[@class="gHead01 all-width data-list"]'

        # 테이블명을 _을 기준으로 나눠 리스트를 만든다.
        title_list = self.title.split('_')
        self.logger.debug(title_list)

        # dataframe 리스트를 만든다.
        df_list = []
        for i in range(2):
            # 상위테이블 0, 하위테이블 1
            df_list.append(common.get_df_from_html(html, table_xpath, i))
        self.logger.debug(df_list)

        # 테이블명리스트와 df리스트를 매치하여 데이터베이스에 저장하기 위해 yield시킴
        for title, df in list(zip(title_list, df_list)):
            # df를 log로 출력한다.
            self.logger.info(title)
            self.logger.debug(df)
            # make item to yield
            item = items.C104items()
            item['코드'] = code
            item['title'] = title
            item['df'] = df
            yield item

    @abstractmethod
    def setting_page(self, url: str):
        pass

    def __del__(self):
        if self.driver is not None:
            print(f'Retrieve {self.name} chrome driver...')
            self.driver.quit()


'''
# XPATH 상수
수익성 = '//*[ @id="val_tab1"]'
성장성 = '//*[ @id="val_tab2"]'
안정성 = '//*[ @id="val_tab3"]'
활동성 = '//*[ @id="val_tab4"]'

연간 = '//*[@id="frqTyp0"]'
분기 = '//*[@id="frqTyp1"]'
검색 = '//*[@id="hfinGubun"]'

가치분석연간 = '//*[@id="frqTyp0_2"]'
가치분석분기 = '//*[@id="frqTyp1_2"]'
가치분석검색 = '//*[@id="hfinGubun2"]'
'''


class C104AQ(C104Spider):
    name = 'c104_aq'

    def __init__(self, code):
        super(C104AQ, self).__init__(code, title='수익성q_가치분석q')

    def setting_page(self, url: str):
        buttons = [
            ('수익성', '//*[ @id="val_tab1"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
            ('가치분석분기', '//*[@id="frqTyp1_2"]'),
            ('가치분석검색', '//*[@id="hfinGubun2"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104BQ(C104Spider):
    name = 'c104_bq'

    def __init__(self, code):
        super(C104BQ, self).__init__(code, title='성장성q')

    def setting_page(self, url: str):
        buttons = [
            ('성장성', '//*[ @id="val_tab2"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104CQ(C104Spider):
    name = 'c104_cq'

    def __init__(self, code):
        super(C104CQ, self).__init__(code, title='안정성q')

    def setting_page(self, url: str):
        buttons = [
            ('안정성', '//*[ @id="val_tab3"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104DQ(C104Spider):
    name = 'c104_dq'

    def __init__(self, code):
        super(C104DQ, self).__init__(code, title='활동성q')

    def setting_page(self, url: str):
        buttons = [
            ('활동성', '//*[ @id="val_tab4"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104AY(C104Spider):
    name = 'c104_ay'

    def __init__(self, code):
        super(C104AY, self).__init__(code, title='수익성y_가치분석y')

    def setting_page(self, url: str):
        buttons = [
            ('수익성', '//*[ @id="val_tab1"]'),
            ('연간', '//*[@id="frqTyp0"]'),
            ('검색', '//*[@id="hfinGubun"]'),
            ('가치분석연간', '//*[@id="frqTyp0_2"]'),
            ('가치분석검색', '//*[@id="hfinGubun2"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104BY(C104Spider):
    name = 'c104_by'

    def __init__(self, code):
        super(C104BY, self).__init__(code, title='성장성y')

    def setting_page(self, url: str):
        buttons = [
            ('성장성', '//*[ @id="val_tab2"]'),
            ('연간', '//*[@id="frqTyp0"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104CY(C104Spider):
    name = 'c104_cy'

    def __init__(self, code):
        super(C104CY, self).__init__(code, title='안정성y')

    def setting_page(self, url: str):
        buttons = [
            ('안정성', '//*[ @id="val_tab3"]'),
            ('연간', '//*[@id="frqTyp0"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)


class C104DY(C104Spider):
    name = 'c104_dy'

    def __init__(self, code):
        super(C104DY, self).__init__(code, title='활동성y')

    def setting_page(self, url: str):
        buttons = [
            ('활동성', '//*[ @id="val_tab4"]'),
            ('연간', '//*[@id="frqTyp0"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ]
        common.click_buttons(self.driver, url, buttons, self.WAIT)
