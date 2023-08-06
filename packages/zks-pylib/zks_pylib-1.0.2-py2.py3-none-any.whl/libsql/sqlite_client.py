#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sqlite3
import json

from libconv.py_conv import *
from libutil.logger import *

'''
sqlite 조회, 저장 관리
sqlite 특성상, connection 객체를 관리할지 관리하지 않을지 선택 필요
다만 접근 인터페이스는 하나가 좋겠음.
'''
class SqliteClient:

    def __init__(self):

        pass

    #static, 단건 수행, 단건, bulk 두개 지원
    #대부분은 Insert 단건 또는 Delete 쿼리로 예상
    #아래 패턴으로 Insert INSERT INTO StockCsvCodeDB (NO, STOCK_CODE, STOCK_NAME) VALUES(?, ?, ?)
    #TODO: bulk 라고 해도 동일하다. 
    #https://stackoverflow.com/questions/18219779/bulk-insert-huge-data-into-sqlite-using-python
    @staticmethod
    def ExecuteQuery(strSQLFilePath, strStatementQuery, tupleData):

        #TODO: isolation_level 이게 지정안되니 , 저장이 안되는듯 하다.
        conn = sqlite3.connect(strSQLFilePath, isolation_level = None)

        cursor = conn.cursor()

        #TODO: bulk 일때는 list 형태, 단건일때는 tuple 형태
        cursor.execute(strStatementQuery, tupleData)
        conn.close()
        pass

    #bulkinsert, 다른가..
    @staticmethod
    def ExecuteMany(strSQLFilePath, strStatementQuery, lstArgs):

        #TODO: isolation_level 이게 지정안되니 , 저장이 안되는듯 하다.
        conn = sqlite3.connect(strSQLFilePath, isolation_level = None)

        cursor = conn.cursor()

        #TODO: bulk 일때는 list 형태, 단건일때는 tuple 형태
        cursor.executemany(strStatementQuery, lstArgs)
        conn.close()
        pass


    #sqlite, 종속성을 제거하는 모델
    #데이터가 많을경우, 향후 cursor 모델도 추가
    #데이터를 조회후, List에 담는다. (한개라도, List로 담는다.)
    #TODO: 소스의 관리적인 차원보다 실용적인 차원, 리펙토링은 나중에.
    @staticmethod
    def QueryForList(strSQLFilePath, strStatementQuery, lstArgs):

        conn = sqlite3.connect(strSQLFilePath)

        conn.text_factory = str
        conn.row_factory = sqlite3.Row 

        rows = []

        #전체를 조회, 결과를 반환 => python으로 있는지 조사 필요.
        #우선 테스트
        with conn:

            cursor = conn.cursor()

            #어라라.. Execute와 같네..
            cursor.execute(strStatementQuery, lstArgs)

            #이미 반환하네...
            rows = cursor.fetchall() #TODO: rows 반환

            #sqlite.rowobject 로 반환 => 하지만 iterator가 되는지 확인

            #별로 좋지 않아 보이는 쿼리.
            # for row in rows :
            #     #strRow = json.dumps( [dict(row) for ix in rows] )
            #     #printf("%s", json.dumps(dict(row)))

            #     dictRow = dict(row)
            #     #LOG().debug(dictRow)
            #     #printf("%s", dictRow)

            #     #strStockName = dictRow.get("STOCK_NAME")
            #     #LOG().debug("종목명=%s", strStockName)
            #     #LOG().debug(json.dumps(dict(row)))
                
            #     '''
            #     strRow = ""
            #     for key in dictRow:
            #         value = dictRow.get(key)
            #         #LOG().debug("%s = %s", key, value)
            #         strRow += "%s = %s " % (key, value)
                
            #     printf("%s", strRow)
            #     '''
            #     #csv로 출력
            #     #header
            #     #strHeader = ",".join(dictRow.keys())
            #     #value
            #     #strValue = ",".join(dictRow.values())
            #     #LOG().debug(strValue)

        #with, 불필요.
        #con.close()

        return rows #어떤 영향을 미칠지...



