"""new nfs mongodb manager

mongodb atlas 를 manage 하는 클래스 모음
"""
import pandas as pd
import pymongo
from pymongo import errors
import datetime
from typing import Tuple
from util_hj3415 import utils
from dart_hj3415 import opendart

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

ATLAS_ADDR = "mongodb+srv://hj3415:piyrw421@nfs.2mnb4.mongodb.net/005930?retryWrites=true&w=majority"
LOCAL_ADDR = 'mongodb://localhost:27017'


def connect_mongo(addr: str, timeout=5):
    # 클라이언트 한개로 데이터베이스를 다루는게 효율적이라 함수를 따로 뺐음.

    # resolve conn error - https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
    import certifi
    ca = certifi.where()
    if addr.startswith('mongodb'):
        # set a some-second connection timeout
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000, tlsCAFile=ca)
        try:
            srv_info = client.server_info()
            conn_str = f"Connect to Mongo Atlas v{srv_info['version']}..."
            print(conn_str, f"Server Addr : {addr}")
            return client
        except Exception:
            conn_str = f"Unable to connect to the server.(MY IP : {utils.get_ip_addr()})"
            raise Exception(f"{conn_str} Server Addr : {addr}")


class Atlas:
    def __init__(self, client):
        self.client = client
        self._db = None
        self._col = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db):
        if self.client is None:
            raise Exception("You should set server connection first")
        else:
            self._db = db

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        if self.db is None:
            raise Exception("You should set database first.")
        else:
            self._col = col

    # ========================End Properties=======================

    def chk_db(self):
        if self._db in self.client.list_database_names():
            return True
        else:
            raise Exception(f'Invalid database name : {self.db}')

    def chk_col(self):
        if self.chk_db():
            if self._col in self.client[self._db].list_collection_names():
                return True
            else:
                raise Exception(f'Invalid collection name : {self.col}')

    def get_all_db(self) -> list:
        return sorted(self.client.list_database_names())

    def get_cols_in_db(self) -> list:
        if self.chk_db():
            return sorted(self.client[self.db].list_collection_names())

    def get_docs(self, remove_id=True) -> list:
        if self.chk_col():
            items = []
            if remove_id:
                for doc in self.client[self.db][self.col].find({}):
                    del doc['_id']
                    items.append(doc)
            else:
                items = list(self.client[self.db][self.col].find({}))
            return items

    def drop_db(self, db: str):
        self.db = db
        if self.chk_db():
            self.client.drop_database(self.db)
            print(f"Drop '{self.db}' database..")

    def clear_db(self):
        for col in self.get_cols_in_db():
            self.client[self.db].drop_collection(col)
        print(f"Delete all collection in {self.db} database..")

    def drop_col(self):
        if self.chk_col():
            self.client[self.db].drop_collection(self.col)
            print(f"Drop {self.col} collection..")

    def clear_col(self):
        if self.chk_col():
            self.client[self.db][self.col].delete_many({})
            print(f"Delete all doccument in {self.col} collection..")

    def initiate_db(self):
        # 데이터베이스 초기화 코드
        for db in self.get_all_db():
            try:
                self.drop_db(db)
            except errors.OperationFailure:
                # 보호된 admin 컬렉션 같은 것은 넘어간다.
                continue


class MI(Atlas):
    """mi 데이터베이스 클래스

    Note:
        db - mi\n
        col - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx' - 총 13개\n
        doc - date, value\n
    """
    MI_DB = 'mi'
    COL_TITLE = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
                 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def __init__(self, client, index: str):
        super(MI, self).__init__(client)
        self.db = self.MI_DB
        self.index = index

    @property
    def index(self):
        return self.col

    @index.setter
    def index(self, index: str):
        if self.db != self.MI_DB:
            self.db = self.MI_DB
        if index in self.COL_TITLE:
            logger.debug(f'Set col : {self.col} -> {index}')
            self.col = index
        else:
            raise Exception(f'Invalid index : {index}({self.COL_TITLE})')

    # ========================End Properties=======================

    def get_recent(self) -> Tuple[str, float]:
        """저장된 가장 최근의 값을 반환하는 함수
        """
        if self.chk_col():
            d = self.client[self.db][self.index].find({'date': {'$exists': True}}).sort('date',
                                                                                        pymongo.DESCENDING).next()
            del d['_id']
            return d['date'], d['value']

    def save(self, mi_dict: dict, index=None) -> bool:
        """MI 데이터 저장

        Args:
            mi_dict (dict): ex - {'date': '2021.07.21', 'value': '1154.50'}
            index (str, optional): 13개의 컬렉션.
        """
        if index is not None:
            self.index = index
        if self.index is None:
            raise Exception("You should set index first.")
        self.client[self.db][self.index].create_index('date', unique=True)
        result = self.client[self.db][self.index].update_one(
            {'date': mi_dict['date']}, {"$set": {'value': mi_dict['value']}}, upsert=True)
        return result.acknowledged

    def drop_db(self, db: str = 'mi'):
        super(MI, self).drop_db(db)


class NotiHx(Atlas):
    """텔레그램 노티한 공시자료 저장 클래스

    dart를 분석하여 유의미한 공시들은 텔레그램으로 노티하며 본 클래스를 통해 데이터베이스에 저장한다.

    """
    NOTI_DB = 'noti'

    # COL의 형식은 %Y%m

    def __init__(self, client):
        super(NotiHx, self).__init__(client)
        self.db = self.NOTI_DB

    @property
    def Ym(self):
        return self.col

    @Ym.setter
    def Ym(self, Ym):
        if self.db != self.NOTI_DB:
            self.db = self.NOTI_DB
        import re
        p = re.compile('^20[0-9][0-9][0,1][0-9]$')
        if p.match(Ym) is None:
            raise ValueError(f'Invalid date format : {Ym}(ex-202010(%Y%m))')
        else:
            self.col = Ym

    # ========================End Properties=======================

    def save(self, noti_dict: dict) -> bool:
        """

        Args:
            noti_dict (dict) : dart 에서 전달되는 딕셔너리 구조

        Note:
            noti_dict 구조\n
            {'code': '005930',\n
            'rcept_no': '20210514000624',\n
            'rcept_dt': '20210514',\n
            'report_nm': '임원ㆍ주요주주특정증권등소유상황보고서',\n
            'point': 2,\n
            'text': '등기임원이 1.0억 이상 구매하지 않음.'}\n
        """
        self.Ym = noti_dict['rcept_dt'][:6]
        self.client[self.db][self.Ym].create_index('rcept_no', unique=True)
        try:
            result = self.client[self.db][self.Ym].insert_one(noti_dict)
        except errors.DuplicateKeyError:
            self.client[self.db][self.Ym].delete_many({'rcept_no': {"$eq": noti_dict['rcept_no']}})
            result = self.client[self.db][self.Ym].insert_one(noti_dict)
        return result.acknowledged

    def load_df(self, Ym: str) -> pd.DataFrame:
        self.Ym = Ym
        try:
            df = pd.DataFrame(self.get_docs())
        except KeyError:
            df = pd.DataFrame()
        return df


class DateBase(Atlas):
    @property
    def date(self):
        return self.col

    @date.setter
    def date(self, date: str):
        if utils.isYmd(date):
            self.col = date
        else:
            raise Exception(f"Invalid date : {date}(%Y%m%d)")

    # ========================End Properties=======================

    def save_df(self, df: pd.DataFrame) -> bool:
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False

        self.clear_col()
        print(f"Save new data to '{self.db}' / '{self.col}'")
        result = self.client[self.db][self.date].insert_many(df.to_dict('records'))
        return result.acknowledged

    def load_df(self) -> pd.DataFrame:
        try:
            df = pd.DataFrame(list(self.client[self.db][self.date].find({}))).drop(columns=['_id'])
        except KeyError:
            df = pd.DataFrame()
        return df


class DartWithDate(DateBase):
    """각 날짜별로 만들어진 공시 데이터프레임을 관리하는 클래스
    """
    DART_DB = 'dart'

    def __init__(self, client, date: str):
        super(DartWithDate, self).__init__(client)
        self.db = self.DART_DB
        self.date = date
        self.client[self.db][self.date].create_index('rcept_no', unique=True)

    def save_df(self, df: pd.DataFrame) -> bool:
        return super().save_df(df)

    def load_df(self, title: str = '') -> pd.DataFrame:
        """저장된 공시 데이터를 데이터프레임으로 반환한다.

        title 인자를 넣으면 타이틀에 해당하는 데이터프레임을 필터링해서 반환한다.
        """
        df = super().load_df()
        if title != '':
            try:
                df = df[df['report_nm'].str.contains(title)]
            except KeyError:
                df = pd.DataFrame()
        return df


class EvalWithDate(DateBase):
    """각 날짜별로 만들어진 eval-report 데이터프레임을 관리하는 클래스
        """
    EVAL_DB = 'eval'

    def __init__(self, client, date: str):
        super(EvalWithDate, self).__init__(client)
        self.db = self.EVAL_DB
        self.date = date
        # 추후 인덱스 설정 필요
        # self.client[self.db][self.date].create_index('rcept_no', unique=True)

    def save_df(self, df: pd.DataFrame) -> bool:
        return super().save_df(df)


class Corps(Atlas):
    """mongodb에 저장된 재무데이터를 가져오는 클래스

    Note:
    <<구조>>\n
        데이터베이스 - 6자리 코드명\n
        컬렉션 -\n
        c101, c106yq, c108, dart\n
        c103손익계산서qy,\n
        c103재무상태표qy,\n
        c103현금흐름표qy,\n
        c104qy,\n
        도큐멘트참고\n
        - c104는 중복되는 항목이 없어 2개의 페이지로 나눔\n
        - c103는 중복되는 항목이 있어 6개의 페이지로 나눔\n
    """
    COL_TITLE = ('c101', 'c104y', 'c104q', 'c106y', 'c106q', 'c108',
                 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',
                 'dart', 'etc')

    @property
    def code(self):
        return self.db

    @code.setter
    def code(self, code: str):
        if utils.is_6digit(code):
            self.db = code
        else:
            raise Exception(f'Invalid value : {code}')

    @property
    def page(self):
        return self.col

    @page.setter
    def page(self, page: str):
        if page in self.COL_TITLE:
            self.col = page
        else:
            raise Exception(f'Invalid value : {page}({self.COL_TITLE})')

    # ========================End Properties=======================

    def get_all_corps(self) -> list:
        """데이터베이스내의 모든 6자리 숫자 코드의 db 명 반환

        """
        corp_list = []
        for db in self.get_all_db():
            if utils.is_6digit(db):
                corp_list.append(db)
        return sorted(corp_list)

    def drop_all_corps(self):
        corp_list = self.get_all_corps()
        for corp_db in corp_list:
            self.drop_db(corp_db)

    def _save_df(self, df: pd.DataFrame) -> bool:
        # c103, c104, c106, c108에서 주로 사용하는 저장방식
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False
        result = self.client[self.code][self.page].insert_many(df.to_dict('records'))
        return result.acknowledged

    def _save_dict(self, dict_data: dict, del_query: dict) -> bool:
        # c101, cdart에서 주로 사용하는 저장방식
        try:
            result = self.client[self.code][self.page].insert_one(dict_data)
        except errors.DuplicateKeyError:
            self.client[self.code][self.page].delete_many(del_query)
            result = self.client[self.code][self.page].insert_one(dict_data)
        return result.acknowledged

    def _load_df(self) -> pd.DataFrame:
        # cdart와 c106에서 주로 사용
        try:
            df = pd.DataFrame(self.get_docs())
        except KeyError:
            df = pd.DataFrame()
        return df


class C101(Corps):
    def __init__(self, client, code: str):
        super(C101, self).__init__(client)
        self.code = code
        self.page = 'c101'
        self.client[self.code][self.page].create_index('date', unique=True)

    def save(self, c101_data: dict) -> bool:
        """

        c101의 구조에 맞는 딕셔너리값을 받아서 구조가 맞는지 확인하고 맞으면 저장한다.

        Note:
            <c101_struc>\n
            'date', '코드', '종목명',\n
            '업종', '주가', '거래량',\n
            'EPS', 'BPS', 'PER',\n
            '업종PER', 'PBR', '배당수익률',\n
            '최고52주', '최저52주', '거래대금',\n
            '시가총액', '베타52주', '발행주식',\n
            '유통비율', 'intro'\n
        """
        c101_struc = ['date', '코드', '종목명', '업종', '주가', '거래량', 'EPS', 'BPS', 'PER', '업종PER', 'PBR', '배당수익률',
                      '최고52주', '최저52주', '거래대금', '시가총액', '베타52주', '발행주식', '유통비율', 'intro']
        # 리스트 비교하기
        # reference from https://codetorial.net/tips_and_examples/compare_two_lists.html
        if c101_data['코드'] != self.code:
            raise Exception("Code isn't equal input data and db data..")
        logger.debug(c101_data.keys())
        if sorted(c101_struc) == sorted(c101_data.keys()):
            # 스크랩한 날짜 이후의 데이터는 조회해서 먼저 삭제한다.
            del_query = {'date': {"$gte": c101_data['date']}}
            return super(C101, self)._save_dict(c101_data, del_query)
        else:
            raise Exception('Invalid c101 dictionary structure..')

    def find(self, date: str) -> dict:
        """

        해당 날짜의 데이터를 반환한다.
        만약 리턴값이 없으면 {} 을 반환한다.

        Args:
            date (str): 예 - 20201011(6자리숫자)
        """
        if utils.isYmd(date):
            converted_date = date[:4] + '.' + date[4:6] + '.' + date[6:]
        else:
            raise Exception(f'Invalid date format : {date}(ex-20201011(8자리숫자))')
        d = self.client[self.code][self.page].find_one({'date': converted_date})
        if d is None:
            return {}
        else:
            del d['_id']
            return d

    def get_all(self) -> list:
        """

        저장된 모든 데이터를 딕셔너리로 가져와서 리스트로 포장하여 반환한다.
        """
        items = []
        for doc in self.client[self.code][self.page].find({'date': {'$exists': True}}).sort('date', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> dict:
        """저장된 데이터에서 가장 최근 날짜의 딕셔너리를 반환한다.

        Examples:
            {'date': '2021.08.09',\n
            '코드': '005930',\n
            '종목명': '삼성전자',\n
            '업종': '반도체와반도체장비',\n
            '주가': '81500',\n
            '거래량': '15522600',\n
            'EPS': 4165.0,\n
            'BPS': 39126.0,\n
            'PER': 19.57,\n
            '업종PER': '17.06',\n
            'PBR': 2.08,\n
            '배당수익률': '3.67',\n
            '최고52주': '96800',\n
            '최저52주': '54000',\n
            '거래대금': '1267700000000',\n
            '시가총액': '486537300000000',\n
            '베타52주': '0.92',\n
            '발행주식': '5969782550',\n
            '유통비율': '74.60',\n
            'intro': '한국 및 CE... DP사업으로 구성됨.'}\n
        """
        try:
            d = self.client[self.code][self.page].find({'date': {'$exists': True}}).sort('date',
                                                                                         pymongo.DESCENDING).next()
            del d['_id']
        except StopIteration:
            d = {}
        return d


class CEtc(Corps):
    def __init__(self, client, code: str):
        super(CEtc, self).__init__(client)
        self.code = code
        self.page = 'etc'
        self.client[self.code][self.page].create_index('항목', unique=True)


class CRefresh(CEtc):
    # 한번 등록되면 리프레시 되는 횟수
    COUNTER = 10

    def __init__(self, client, code: str):
        super(CRefresh, self).__init__(client, code)

    def set_count(self, date: str) -> bool:
        """
        'etc' 컬렉션에 다음과 같이 카운트를 세팅하여 저장한다.
        {'항목': 'refresh', 'count': 10, 'date': '20211010'}
        """
        if not utils.isYmd(date):
            raise Exception(f'Invalid date format : {date}(%Y%m%d)')

        print(f"Setting refresh doc ... 'count': {self.COUNTER}, 'date': {date}")
        result = self.client[self.code][self.page].update_one(
            {'항목': 'refresh'}, {"$set": {'count': self.COUNTER, 'date': date}}, upsert=True)
        return result.acknowledged

    def count_down(self) -> bool:
        """
        데이터베이스의 카운트를 확인하고 0이하면 삭제 0 이상이면 1을 줄인다.
        """
        doc = self.client[self.code][self.page].find_one({'항목': 'refresh'})
        if doc is None or (doc['count'] <= 0):
            self.initiate()
            return False
        else:
            print(f"Counting down...{doc['count']} -> {doc['count']-1}")
            self.client[self.code][self.page].update_one({'항목': 'refresh'}, {"$inc": {'count': - 1}})
            return True

    def initiate(self):
        print("Initialting refresh doc ... {'count': 0, 'date': None}")
        self.client[self.code][self.page].update_one(
            {'항목': 'refresh'}, {"$set": {'count': 0, 'date': None}}, upsert=True)


class CDart(Corps):
    """각 Code 별로 분류된 Dart 를 관리하는 클래스
    """

    def __init__(self, client, code: str):
        super(CDart, self).__init__(client)
        self.code = code
        self.page = 'dart'
        self.client[self.code][self.page].create_index('rcept_no', unique=True)

    def save(self, dart_data: dict) -> bool:
        """
        Args:
            dart_data (dict) : dart 에서 전달되는 딕셔너리 구조

        Note:
            dart_data 구조\n
            {'rcept_no': '20210514000624',\n
            'rcept_dt': '20210514',\n
            'report_nm': '임원ㆍ주요주주특정증권등소유상황보고서',\n
            'point': 2,\n
            'text': '등기임원이 1.0억 이상 구매하지 않음.',\n
            'is_noti': True}\n
        """
        del_query = {'rcept_no': {"$eq": dart_data['rcept_no']}}
        return super(CDart, self)._save_dict(dart_data, del_query)

    def load(self) -> pd.DataFrame:
        return super()._load_df()

    def cleaning_data(self, days_ago: int = 180):
        """
        days_ago 인자를 기준으로 이전 날짜의 데이터를 검색하여 삭제한다.
        본 함수를 주기적으로 실행해 준다.
        """
        border_date_str = (datetime.datetime.today() - datetime.timedelta(days=days_ago)).strftime('%Y%m%d')
        logger.debug(f'boder_date : {border_date_str}')
        try:
            self.client[self.code][self.page].delete_many({'rcept_dt': {'$lt': border_date_str}})
            logger.debug(f'Delete dart data before {days_ago} days ago..')
        except:
            logger.error(f'Error occurred while delete dart data..')


class C106Y(Corps):
    def __init__(self, client, code: str):
        """

         Args:
            code (str): 종목코드(디비명)
            page (str): c106y
        """
        super(C106Y, self).__init__(client)
        self.code = code
        self.page = 'c106y'

    def save(self, c106_data: pd.DataFrame) -> bool:
        self.client[self.code][self.page].create_index('항목', unique=True)
        self.clear_col()
        return super(C106Y, self)._save_df(c106_data)

    def load(self) -> pd.DataFrame:
        return super(C106Y, self)._load_df()


class C106Q(Corps):
    def __init__(self, client, code: str):
        """

         Args:
            code (str): 종목코드(디비명)
            page (str): c106q
        """
        super(C106Q, self).__init__(client)
        self.code = code
        self.page = 'c106q'

    def save(self, c106_data: pd.DataFrame) -> bool:
        self.client[self.code][self.page].create_index('항목', unique=True)
        self.clear_col()
        return super(C106Q, self)._save_df(c106_data)

    def load(self) -> pd.DataFrame:
        return super(C106Q, self)._load_df()


class C108(Corps):
    def __init__(self, client, code: str):
        super(C108, self).__init__(client)
        self.code = code
        self.page = 'c108'

    def save(self, c108_data: pd.DataFrame) -> bool:
        self.client[self.code][self.page].insert_one({})
        self.clear_col()
        return super(C108, self)._save_df(c108_data)

    def get_all(self) -> list:
        """

        저장된 모든 데이터를 딕셔너리로 가져와서 리스트로 포장하여 반환한다.
        """
        items = []
        for doc in self.client[self.code][self.page].find({'날짜': {'$exists': True}}).sort('날짜', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> list:
        """

        저장된 데이터에서 가장 최근 날짜의 딕셔너리를 가져와서 리스트로 포장하여 반환한다.

        Returns:
            list: 한 날짜에 c108 딕셔너리가 여러개 일수 있어서 리스트로 반환한다.
        """
        # 저장되어 있는 데이터베이스의 최근 날짜를 찾는다.
        try:
            r_date = \
            self.client[self.code][self.page].find({'날짜': {'$exists': True}}).sort('날짜', pymongo.DESCENDING).next()[
                '날짜']
        except StopIteration:
            # 날짜에 해당하는 데이터가 없는 경우
            return []

        # 찾은 날짜를 바탕으로 데이터를 검색하여 리스트로 반환한다.
        r_list = []
        for r_c108 in self.client[self.code][self.page].find({'날짜': {'$eq': r_date}}):
            del r_c108['_id']
            r_list.append(r_c108)
        return r_list


class C1034(Corps):
    pass


class C103(C1034):
    """C103 컬렉션 관련 클래스
    """

    def __init__(self, client, code: str, page: str):
        """

        Args:
            code (str): 종목코드(디비명)
            page (str): 페이지명(컬렉션명)

        Example:
            c103손익계산서q\n
            c103재무상태표y\n
            c103현금흐름표q\n

        """
        super(C103, self).__init__(client)
        self.code = code
        self.page = page

    def save(self, c103_data: pd.DataFrame) -> bool:
        """데이터베이스에 저장

        Example:
            c103_list 예시\n
            [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
            {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        self.client[self.code][self.page].create_index('항목', unique=False)
        self.clear_col()
        return super(C103, self)._save_df(c103_data)


class C104(C1034):
    """C104 컬렉션 관련 클래스
    """

    def __init__(self, client, code: str, page: str):
        """

        Args:
            code (str): 종목코드(디비명)
            page (str): c104y, c104q(컬렉션명)
        """
        super(C104, self).__init__(client)
        self.code = code
        self.page = page

    def save(self, c104_data: pd.DataFrame) -> bool:
        """데이터베이스에 저장

        c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에
        stamp 를 검사하여 12시간 전보다 이전에 저장된 자료가 있으면
        삭제한 후 저장하고 12시간 이내의 자료는 삭제하지 않고
        데이터를 추가하는 형식으로 저장한다.

        Example:
            c104_data 예시\n
            [{'항목': '매출액증가율',...'2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율',...'2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        self.client[self.code][self.page].create_index('항목', unique=True)
        time_now = datetime.datetime.now()
        try:
            stamp = self.client[self.code][self.page].find_one({'항목': 'stamp'})['time']
            if stamp < (time_now - datetime.timedelta(days=.5)):
                # 스템프가 12시간 이전이라면..연속데이터가 아니라는 뜻이므로 컬렉션을 초기화한다.
                self.clear_col()
        except TypeError:
            # 스템프가 없다면...
            pass
        # 항목 stamp를 찾아 time을 업데이트하고 stamp가 없으면 insert한다.
        self.client[self.code][self.page].update_one({'항목': 'stamp'}, {"$set": {'time': time_now}}, upsert=True)
        return super(C104, self)._save_df(c104_data)

    def modify_stamp(self, days_ago: int):
        # 인위적으로 타임스템프를 수정한다 - 테스트 용도
        try:
            before = self.client[self.code][self.page].find_one({'항목': 'stamp'})['time']
        except TypeError:
            # 이전에 타임스템프가 없는 경우
            before = None
        time_2da = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        self.client[self.code][self.page].update_one({'항목': 'stamp'}, {"$set": {'time': time_2da}}, upsert=True)
        after = self.client[self.code][self.page].find_one({'항목': 'stamp'})['time']
        print(f"Stamp changed: {before} -> {after}")


# ================================= 준비중 =====================================


class C1034_Old(Corps):

    def get_all_title(self) -> list:
        """

        중복된 타이틀을 취급하지 않기 위해 타이틀 전체에서 중복된 타이틀을 제거하고 나머지 타이틀 리스트를 반환한다.

        Returns:
            list: 중복된 항목을 제외한 모든 항목을 담은 리스트
        """
        # 항목만 추출한 리스트 만들기
        title_list = []
        for item_dict in self.get_all_item():
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                pass
            else:
                title_list.append(item_dict['항목'])

        # 리스트 중복요소 찾기
        # https://infinitt.tistory.com/78
        count = {}
        for i in title_list:
            try:
                count[i] += 1
            except KeyError:
                count[i] = 1

        # 중복되지 않는 타이틀만으로 리스트를 만들어 반환하기
        return_list = []
        for k, v in count.items():
            if v == 1:
                return_list.append(k)

        return return_list

    def get_all(self) -> dict:
        """

        페이지의 모든 항목에 대한 값을 딕셔너리 형태로 반환.

        Returns:
            dict: 각 항목을 키로하고 해당 기간별 데이터를 값으로 하는 딕셔너리

        Example:
            리턴값 예시\n
            {'*(비지배)당기순이익': {...'2020/12': 1860.0, '2021/12': nan},
            '*(지배)당기순이익': {...'2020/12': 16021.5,'2021/12': nan},}

        """
        c1034_list = self.get_all_item()
        # c104_list 내부에서는 항목, 전년/분기대비, 년/월을 포함하는 딕셔너리가 담겨있다.
        return_dict = {}
        not_duplicated_titles = self.get_all_title()
        for item_dict in c1034_list:
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                continue
            if item_dict['항목'] in not_duplicated_titles:
                # 중복된 타이틀을 뺀 나머지 항목들은 타이틀을 키로 하고 년/월을 값으로 하는 새로운 딕셔너리로 만든다.
                temp_dict = {}
                # 전년/분기대비, 항목타이틀, Unnamed 제거를 위해 새로운 임시 딕셔너리를 만든다.
                for k, v in item_dict.items():
                    if k.startswith('전') or k.startswith('항') or k.startswith('Unnamed'):
                        pass
                    else:
                        temp_dict[k] = v

                if item_dict['항목'] in return_dict.keys():
                    raise KeyError(f"중복된 항목이 있음 : {item_dict['항목']}")
                else:
                    return_dict[item_dict['항목']] = temp_dict
        return return_dict

    def get_all_cmp(self) -> dict:
        """

        페이지의 모든 항목에 대한 전년/분기대비 값을 딕셔너리 형태로 반환.

        Returns:
            dict: 각 항목을 키로하고 전분기/년대비 증감 데이터를 값으로 하는 딕셔너리

        Example:
            리턴값 예시\n
            {'*(비지배)당기순이익': 26.1,
            '*(지배)당기순이익': -12.7,
            '*CAPEX': 8.0}

        """
        c1034_list = self.get_all_item()
        # c104_list 내부에서는 항목, 전년/분기대비, 년/월을 포함하는 딕셔너리가 담겨있다.
        return_dict = {}
        not_duplicated_titles = self.get_all_title()
        for item_dict in c1034_list:
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                continue
            if item_dict['항목'] in not_duplicated_titles:
                temp_dict = {}
                for k, v in item_dict.items():
                    if k.startswith('전'):
                        temp_dict[k] = v
                # temp_dict 에는 {'전년대비': -1.36, '전년대비1': nan} 또는 {'전분기대비': 14.63} 가 담긴다.
                if len(temp_dict) == 1:
                    # {'전분기대비': 14.63}인 경우 ...
                    return_dict[item_dict['항목']] = temp_dict.popitem()[1]
                elif len(temp_dict) == 2:
                    # {'전년대비': -1.36, '전년대비1': nan}인 경우 ...
                    v = temp_dict.pop('전년대비1')
                    if math.isnan(v):
                        return_dict[item_dict['항목']] = temp_dict.pop('전년대비')
                    else:
                        return_dict[item_dict['항목']] = v
                else:
                    # 데이터가 없는 경우는 nan 으로 세팅한다.
                    return_dict[item_dict['항목']] = float('nan')
        return return_dict

    # ========================특정 페이지 관련 함수들=======================

    @staticmethod
    def _nan_to_zero(target: Tuple[str, float]) -> Tuple[str, float]:
        """

        실수형 입력값을 받아 nan인 경우 0으로 변환하여 반환하는 유틸함수.
        """
        return target[0], 0 if math.isnan(target[1]) else target[1]

    def get_stamp(self) -> datetime.datetime:
        return self.client[self.db][self.col].find({'stamp': {'$exists': True}}).next()['stamp']

    def find_cmp(self, title: str) -> float:
        """

        타이틀에 해당하는 전년/분기대비 값을 반환한다.\n
        해당 타이틀이 없을 경우 - nan 반환함.\n

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            float: 전년/분기대비 증감율

        Note:
            중복되는 title 은 취급하지 않기로함.\n
            get_all_title()함수에서 중복 타이틀 정리함.\n
        """
        try:
            return self.get_all_cmp()[title]
        except KeyError:
            return float('nan')

    def find(self, title: str) -> dict:
        """

        타이틀에 해당하는 년도, 분기 딕셔너리를 반환한다.\n
        해당 타이틀이 없을 경우 - {} 반환함.\n

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            dict: ex - {'2016/12': 51.9',...'2019/12': 4.2, '2020/12': 344.1, '2021/12': nan}

        Note:
            중복되는 title 은 취급하지 않기로함.\n
            get_all_title()함수에서 중복 타이틀 정리함.\n
        """
        try:
            return self.get_all()[title]
        except KeyError:
            return {}

    def sum_recent_4q(self, title: str, nan_to_zero: bool = False) -> Tuple[str, float]:
        """최근 4분기 합

        분기 페이지 한정 해당 타이틀의 최근 4분기의 합을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀
            nan_to_zero (bool): 반환값이 nan 인 경우 0으로 바꿀것인지 결정 여부

        Returns:
            tuple: (계산된 4분기 중 최근분기, 총합)

        Raises:
            TypeError: 페이지가 q가 아닌 경우 발생

        Note:
            분기 데이터가 4개 이하인 경우 그냥 최근 연도의 값을 찾아 반환한다.
        """
        if self.col.endswith('q'):
            # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
            # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
            od_q = OrderedDict(sorted(self.find(title=title).items(), reverse=False))
            logger.info(f'{title} : {od_q}')
            if len(od_q) < 4:
                # od_q의 값이 4개 이하이면 그냥 최근 연도의 값으로 반환한다.
                t = C1034(code=self.db, page=self.col[:-1] + 'y').latest_value(title=title)
                if nan_to_zero:
                    return self._nan_to_zero(t)
                else:
                    return t
            else:
                q_sum = 0
                last_date = list(od_q.items())[-1][0]
                for i in range(4):
                    # last = True 이면 최근의 값부터 꺼낸다.
                    d, v = od_q.popitem(last=True)
                    logger.debug(f'd:{d} v:{v}')
                    q_sum += 0 if math.isnan(v) else v
                t = str(last_date), round(q_sum, 2)
                if nan_to_zero:
                    return self._nan_to_zero(t)
                else:
                    return t
        else:
            raise TypeError(f'Not support year data..{self.col}')

    def latest_value(self, title: str, nan_to_zero: bool = False) -> Tuple[str, float]:
        """가장 최근 년/분기 값

        해당 타이틀의 가장 최근의 년/분기 값을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀
            nan_to_zero (bool): 반환값이 nan 인 경우 0으로 바꿀것인지 결정 여부

        Returns:
            tuple: ex - ('2020/09', 39617.5) or ('', 0)

        Note:
            만약 최근 값이 nan 이면 찾은 값 바로 직전 것을 한번 더 찾아 본다.\n
            데이터가 없는 경우 ('', 0) 반환한다.\n
        """
        # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
        # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
        od = OrderedDict(sorted(self.find(title=title).items(), reverse=False))
        logger.info(f'{title} : {od}')
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
            return self._nan_to_zero(tuple(last_one))
        else:
            return tuple(last_one)


if __name__ == "__main__":
    atlas_addr = "mongodb+srv://hj3415:piyrw421@nfs.2mnb4.mongodb.net/005930?retryWrites=true&w=majority"
    local_addr = 'mongodb://localhost:27017'

    client = connect_mongo(atlas_addr)
    Atlas(client).initiate_db()
