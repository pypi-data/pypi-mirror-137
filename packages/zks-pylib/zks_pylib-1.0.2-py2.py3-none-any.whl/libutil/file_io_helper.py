#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from libconv.py_conv import *
from libutil.logger import *

#외부모듈

#FILE 처리 관련, static 객체중심으로 작성

class FileIOHelper:

    def __init__(self):

        pass


    #UTF-8 파일을 읽어서, string으로 변환
    #전체 파일을 읽으므로, 작은 사이즈로 처리해야 함
    #python 버전에 따라 달라짐
    @staticmethod
    def OpenFileAsUTFToStream(sFilePath):

        if None == sFilePath:
            return None

        #TODO: 파일 존재여부 확인, 파일이 없으면 에러.
        #기록모드로 열어야함

        bAccess = os.access(sFilePath, os.W_OK)

        if False == bAccess:
            LOG().error("fail open file, access error path = {}".format(sFilePath))
            return None

        #python 2,3 호환
        return PYCONV().ReadUTF8FileStream(sFilePath)

    
    #데이터를 파일에 저장, PYCONV()를 호출하더라도, 접근은 여기서.
    @staticmethod
    def WriteToUTF8File(strBuffer, strFilePath, encoding="utf-8"):
        return PYCONV().WriteToUTF8File(strBuffer, strFilePath, _encoding = encoding)

    
    
    
