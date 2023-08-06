#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging #logging
import logging.handlers
import os

import pprint #출력 가독성

#Logger singleton 구현

#logger에서만 유일하게 사용
def printf(formt, *args):

    strLog = formt % args
    pprint.pprint(strLog) #print strLog
    #print strLog
    return 0 #End


class LibKLogger:

    #전역 singleton 객체
    __instance = None
    __bCreateSingleton = False #singleton으로 접근 및 생성 여부

    @classmethod
    def GetInstance(cls, *args, **kargs):

        if not cls.__instance:
            cls.__bCreateSingleton = True
            cls.__instance = cls(*args, **kargs)
            #printf("Create Logger Singleton Instance")
        #TODO: 이것은 무엇?
        #cls.instance = cls.__instance

        return cls.__instance
    
    def __new__(cls, *args, **kwargs):

        #TODO: not 이 있지만, 직관적이지 않아서, False, None으로 타입 체크..
        #python 스럽지는 않다.
        if False == cls.__bCreateSingleton: 
          raise Exception("Constructor cannot be create directly, use GetInstance")

        if not hasattr(cls, "_instance"):         # 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # 클래스의 객체를 생성하고 Foo._instance로 바인딩 => 최초 1회만 생성
            #printf("First __new__ Logger")
        else:
            raise Exception("Constructor cannot be create directly, use GetInstance")

        return cls._instance                     
    
    def __init__(self):
        assert not hasattr(self.__class__, '__instance'), 'Do not call constructor directly!'

        #이시점부터 멤버 변수
        self.__logger = None #logger 변수

        #여기까지는 봐주자.
        self.__logger = logging.getLogger('khan-python')
        self.__logger.setLevel(logging.INFO) #INFO LEVEL 기본을 INFO로, DEBUG는 옵션으로
        pass

    #logger 본체 반환
    def GetLogger(self):
        return self.__logger

    #Logger 초기화.
    def InitializeLogger(self, _LogFileName="trace.log", strLogDir = "trace-log", pid=os.getpid()):

        formatter = logging.Formatter("[%(asctime)s][%(process)d][%(filename)s][%(levelname)s] (%(funcName)s:%(lineno)d) %(message)s")

        #로그 저장 경로

        #로그디렉토리, 없으면 자동 생성
        if False == os.path.isdir(strLogDir):
            os.makedirs(strLogDir)

        #TODO: pid는 주지 않는데, pid를 주면, 재시작시 rotation이 되지 않는다.

        strFileName = "{0}/{1}_{2}".format(strLogDir, pid, _LogFileName)
        #strFileName = "trace-log/%s" % _LogFileName

        fileHandler = logging.handlers.RotatingFileHandler(filename=strFileName , maxBytes=(20 * 1024 * 1024), backupCount=10)
        #fileHandler = logging.handlers.RotatingFileHandler(filename='trace-log/trace.log', maxBytes=(4 * 1024 * 1024), backupCount=20)
        #streamHandler = logging.StreamHandler()
        
        #format
        fileHandler.setFormatter(formatter)
        #streamHandler.setFormatter(formatter)

        self.__logger.addHandler(fileHandler)
        #logger.addHandler(streamHandler) #debug용, 화면 출력
        return 0

    #디버그용, 화면에 결과 출력
    def AddStreamLogger(self):

        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] [%(filename)s](%(funcName)s:%(lineno)d) %(message)s")
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self.__logger.addHandler(streamHandler)
        return 0  


    ################################# private

#global logger
#logger.setLevel(logging.DEBUG) #DEBUG LEVEL

#logger반환, 최대한 심플하게 반환
def LOG():
    return LibKLogger.GetInstance().GetLogger()

def InitLogger(_LogFileName="trace.log", strLogDir = "trace-log", pid=os.getpid()):
    LibKLogger.GetInstance().InitializeLogger(_LogFileName, strLogDir, pid)


def AddStreamLogger():
    LibKLogger.GetInstance().AddStreamLogger()






    
    
