#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import json
import sys
import datetime

#LOG 모듈 , 나중에 경로 이동
from libutil.logger import *
from libutil.file_io_helper import *
from libglobal.global_const import *

from libconv.py_conv import *

class JsonHelper:

    def __init__(self):

        #재사용 미검토, 상태 최소화
        #self.__mailTransModule = None #메일 전송 모듈, 재사용을 검토
        pass
    
    #string 을 json으로 load, dictionary에 로드
    @staticmethod
    def LoadToDictionary(strJsonData, dictJsonVal):
        
        #TODO: 결과가 dictionary가 아닐수 있다.
        dictLocalVal = json.loads(strJsonData, strict=False)

        #TODO: list 형태이면 에러 발생. (일단 예외처리 안함)
        dictJsonVal.update(dictLocalVal)
        
        return ERR_OK

    #json을 string으로 변환, 전달 (값복사로 하자)
    #TODO: global 모듈로 이동, static으로 선언?
    @staticmethod
    def JsonFileToDictionary(sFilePath, dictJsonVal):

        #TODO: python 2에서는 encoding이 없음.

        strJsonData = FileIOHelper.OpenFileAsUTFToStream(sFilePath)

        #fJsonFile = open(sFilePath, encoding="utf-8")
        #fJsonFile = open(sFilePath)

        #strJsonData = fJsonFile.read()

        dictLocalVal = json.loads(strJsonData, strict=False)

        #어떻게 복사?
        dictJsonVal.update(dictLocalVal)

        #fJsonFile.close()

        #return 0
        return ERR_OK #완전 독립적으로 사용가능한. 현재는, 향후 logger나 종속은 될 여지 있음

    #특정 데이터의 업데이트

    #map 데이터의 json으로 변환
    @staticmethod
    def WriteMapToJsonFile(dictVal, strJsonFilePath, openOpt="w", encoding="utf-8", bIndent=True, _indent=4, bAppendCRLF=True):

        #TODO: python2, python3 호환코드 => 이것도 고민

        strJsonLog = JsonHelper.GetJsonString(dictVal, bIndent, _indent)

        if True == bAppendCRLF:
            strJsonLog += "\r\n"

        #파일로 저장 (저장옵션 python2 3 다름, UTF-8)
        PYCONV().WriteToUTF8File(strJsonLog, strJsonFilePath, openOpt, encoding)    

        return ERR_OK    

    #test메소드 추가, dictionary = json, 그대로 출력
    @staticmethod
    def PrintDumpJsonLog(dictVal, bIndent=True, _indent=4):

        strJsonLog = JsonHelper.GetJsonString(dictVal, bIndent, _indent)

        LOG().debug(strJsonLog)
        
        return ERR_OK
    

    #... static으로 한걸 후회..
    @staticmethod
    def GetJsonString(dictVal, bIndent, _indent):

        #TODO: python2, python3 호환코드 => 이것도 고민
        
        #indent 기본 4로 지정 (이정도는 괜찮을듯)
        #strJsonLog = json.dumps(dictVal, ensure_ascii=False, indent=4)
        
        
        #예외처리를 위해서, 내부 함수를 추가
        def json_default(value): 
            if isinstance(value, datetime.date): 
                return value.strftime('%Y-%m-%d') 
            #raise TypeError('not JSON serializable') 

        strJsonLog = ""
        if True == bIndent:        
            strJsonLog = json.dumps(dictVal, ensure_ascii=False, indent=_indent)
        else:
            strJsonLog = json.dumps(dictVal, ensure_ascii=False, default=json_default)

        #LOG().debug("jsonlog = {}".format(strJsonLog))

        return  strJsonLog
    