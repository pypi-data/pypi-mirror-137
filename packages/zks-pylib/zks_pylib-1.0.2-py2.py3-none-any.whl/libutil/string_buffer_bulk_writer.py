#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback

import threading #tid 가져오기 위해 선언
import time
import datetime

#외부 라이브러리
from libutil.logger import *
from libglobal.global_const import *

from libjson.json_helper import JsonHelper
from libutil.file_io_helper import FileIOHelper
from libconv.py_conv import * #python2, pytho3 호환


'''
string 버퍼에 로그를 담고, 정해진 주기마다 기록한다.
주기마다 기록시 스레드 스케쥴러에 담을수도 있다. 
우선 단일 스레드 환경에서 정해진 주기로 write 하는 모듈을 개발한다.
TMS로직이 들어가서 범용적으로 사용은 못한다. 일단 util에서 관리
'''

class StringBufferBulkWriter:

    def __init__(self):

        self.__strBuffer = None #문자 버퍼
        self.__nWriteCount = 0 #최대 버퍼 제한값

        self.__dictBulkOpt = None #config option

        #임시경로, Bulk 경로
        self.__strTempFileFullPath = ""
        self.__strBulkFileFullPath = ""

        self.__WRITE_LIMIT = 0 #저장 제한값 (빈번해서 별도 변수로 분리)

        pass


    #초기화 모듈, config와 분리를 위해, 밖에서 만들어서 던진다.
    def Initialize(self, dictOpt):
        
        #TODO: 이름 통일하자.

        self.__strBuffer = ""
        self.__nWriteCount = 0
        self.__dictBulkOpt = dictOpt.copy()

        #디렉토리 자동 생성. 소스 통일해야..

        strTempFilePath = self.__dictBulkOpt.get("temp_file_path")
        strBulkFilePath = self.__dictBulkOpt.get("bulk_file_path")

        self.__WRITE_LIMIT = self.__dictBulkOpt.get("max_limit")

        if "/" != strTempFilePath[len(strTempFilePath) -1] :
            strTempFilePath += "/"

        if "/" != strBulkFilePath[len(strBulkFilePath) -1] :
            strBulkFilePath += "/"
        
        if (False == os.path.isdir(strTempFilePath)):
            os.makedirs(strTempFilePath)
            self.__dictBulkOpt["temp_file_path"] = strTempFilePath #혹시모르니 update

        if (False == os.path.isdir(strBulkFilePath)):
            os.makedirs(strBulkFilePath)
            self.__dictBulkOpt["bulk_file_path"] = strBulkFilePath


        self.__InitializeFileWriteState()
        #self.__MakeFileName(self.__strTempFileFullPath, self.__strBulkFileFullPath, self.__dictBulkOpt)

        return ERR_OK


    def WriteLog(self, strLog):

        self.__strBuffer += strLog
        self.__nWriteCount += 1

        #제한값 이상이면, 즉시 저장
        if self.__WRITE_LIMIT <= self.__nWriteCount:
            self.FlushBuffer()
            pass

        return ERR_OK

    #데이터를 저장한다.
    def FlushBuffer(self):

        #버퍼가 비어있으면 종료
        if 0 == len(self.__strBuffer):
            self.__InitializeFileWriteState()
            return ERR_OK


        #파일에 저장
        #TODO: 예외처리 보강
        FileIOHelper.WriteToUTF8File(self.__strBuffer, self.__strTempFileFullPath)

        os.rename(self.__strTempFileFullPath, self.__strBulkFileFullPath)

        #저장이 마무리 되면, 다시 초기화
        self.__InitializeFileWriteState()

        return ERR_OK


    ########################################## private

    #파일 기록상태, 초기화 한다.
    def __InitializeFileWriteState(self):

        self.__strBuffer = ""
        self.__nWriteCount = 0

        self.__strTempFileFullPath = ""
        self.__strBulkFileFullPath = ""

        self.__MakeFileName(self.__dictBulkOpt)

        #LOG().debug("Initialize File Write State, tempfile={}, bulkfile={}".format(self.__strTempFileFullPath, self.__strBulkFileFullPath))

        return ERR_OK

    #파일명, 시작시점에 만들어서, 저장후 다시 생성 (저장시점에 만들면 날짜가 맞지 않을수 있다.)
    #member로 던지면, 값을 변경하면 같이 변경될듯.
    def __MakeFileName(self, dictBulkOpt):
        
        #현재 시간을 가져온다.

        strTempFileDir = dictBulkOpt.get("temp_file_path")
        strBulkFileDir = dictBulkOpt.get("bulk_file_path")
        strCollectionName = dictBulkOpt.get("collection_prefix")

        now = datetime.datetime.now() #오늘날짜

        strDateYMD = now.strftime("%Y%m%d")
        microsecond = now.microsecond

        pid = os.getpid()
        #python2.7 에서 미지원 => 우선 TMS만 지원
        #tid = threading.get_ident()
        #threading._get_ident()
        tid = PYCONV().GetThreadID()
        

        #임시경로#컬렉션명#현재날짜(YMD)#고유값.json
        #추가적인 고유값 필요

        #TODO: 안들어가진다.. 멤버로 관리
        
        self.__strTempFileFullPath = "{tempdir}{collection}#{date}#{msec}#{pid}#{tid}.json".format(
            tempdir = strTempFileDir,
            collection = strCollectionName,
            date = strDateYMD,
            msec = microsecond,
            pid = pid,
            tid = tid
        )

        self.__strBulkFileFullPath = "{bulkdir}{collection}#{date}#{msec}#{pid}#{tid}.json".format(
            bulkdir = strBulkFileDir,
            collection = strCollectionName,
            date = strDateYMD,
            msec = microsecond,
            pid = pid,
            tid = tid
        )

        #LOG().debug("tempfile = {}, destfile = {}".format(strTempFilePath, strBulkFilePath))


        return ERR_OK
