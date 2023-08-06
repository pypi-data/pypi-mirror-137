import time
import pandas as pd
from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def adjust_arg_type(code) -> list:
    """
    커맨드라인에서 스파이더를 실행할 경우 인자 형식이 str 이 되기 때문에 list 로 변경해 주는 함수
    """
    if type(code) is str:
        return [code, ]
    elif type(code) is list:
        return code
    else:
        raise TypeError


def click_buttons(driver: WebDriver, url: str, buttons: List[Tuple[str, str]], wait: float):
    # 하부 클래스에서 buttons 리스트를 입력받아 실제 버튼을 클릭하는 함수
    logger.debug(f'*** Setting {url} page by clicking buttons ***')
    driver.get(url)
    for name, xpath in buttons:
        logger.debug(f'- Click the {name} button')
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(wait)
    logger.debug('*** Buttons click done ***')


def get_df_from_html(selector, xpath, table_num):
    """
    C103,C104에서 사용
    펼치지 않은 네이버 테이블의 항목과 내용을 pandas 데이터프레임으로 변환시킴
    reference from http://hleecaster.com/python-pandas-selecting-data/(pandas 행열 선택)
    reference from https://blog.naver.com/wideeyed/221603778414(pandas 문자열 처리)
    reference from https://riptutorial.com/ko/pandas/example/5745/dataframe-%EC%97%B4-%EC%9D%B4%EB%A6%84-%EB%82%98%EC%97%B4(pandas 열이름 나열)
    """
    # 전체 html source에서 table 부위만 추출하여 데이터프레임으로 변환
    tables_list = selector.xpath(xpath).getall()
    # print(tables_list[table_num])
    df = pd.read_html(tables_list[table_num])[0]
    # 항목열의 펼치기 스트링 제거
    df['항목'] = df['항목'].str.replace('펼치기', '').str.strip()
    # reference from https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex(정규표현식 특수기호처리)
    # 인덱스행의 불필요한 스트링 제거
    df.columns = (df.columns.str.replace('연간컨센서스보기', '', regex=False).str.replace('연간컨센서스닫기', '', regex=False)
                  .str.replace('\(IFRS연결\)', '', regex=True).str.replace('\(IFRS별도\)', '', regex=True)
                  .str.replace('\(GAAP개별\)', '', regex=True).str.replace('\(YoY\)', '', regex=True)
                  .str.replace('\(QoQ\)', '', regex=True).str.replace('\(E\)', '', regex=True)
                  .str.replace('.', '', regex=False).str.strip())
    return df
