#!/usr/bin/python
# -*- coding: utf-8 -*-

#import os
import sys

import ssl
import pymongo
#from pymongo import MongoClient

from libconv.py_conv import *
from libutil.logger import *


#외부모듈

#FILE 처리 관련, static 객체중심으로 작성
#가급적 무상태 패턴
class MongoDBConnectionHelper:

    #MONGO_SSL_CONFIG_ENABLE = 1 #TMS config, ssl 사용 여부

    def __init__(self):

        pass

    #Mongodb, TMS쪽 로직 추가.
    def GetTMSMongoClient(self, strMongoDBIP, nMongoDBPort, mongoSSLAuthInfo):

        #mongodb 계정 인증 사용여부
        bUseMongoDBAuth = mongoSSLAuthInfo.bUseMongoDBAuth

		#mongodb 계정 ID, PW
        strMongodbAuthID = mongoSSLAuthInfo.strMongodbAuthID
        strMongodbAuthPasswd = mongoSSLAuthInfo.strMongodbAuthPasswd

		#mongodb SSL 사용여부, ssl 키
        bMongosslEnable = mongoSSLAuthInfo.bMongosslEnable
        strMongosslKeyPath = mongoSSLAuthInfo.strMongosslKeyPath

        #mongodb 계정 인증
        if True == bUseMongoDBAuth:
            LOG().info("enable mongodb authenticate")
            strMongoDBURL = "mongodb://{USERID}:{USERPW}@{MONGOIP}:{MONGOPORT}".format(
            USERID=strMongodbAuthID, USERPW=strMongodbAuthPasswd, MONGOIP=strMongoDBIP, MONGOPORT=nMongoDBPort)
        else:
            strMongoDBURL = "{MONGOIP}:{MONGOPORT}".format(MONGOIP=strMongoDBIP, MONGOPORT=nMongoDBPort)


        LOG().info("connect mongodb, url= {}".format(strMongoDBURL))

        #TODO: try/except
        #mongodb 접속 실패는, 재시도 로직 필요. (무한 재시도)
        
        #SSL, TODO: ssl 설정은 미사용시 적용하면 안됨.
         #https://stackoverflow.com/questions/36314776/pymongo-error-bson-errors-invalidbson-utf8-codec-cant-decode-byte-0xa1-in-p
        if True == bMongosslEnable:

            LOG().info("enable mongodb ssl key={}".format(strMongosslKeyPath))

            if None == strMongosslKeyPath or "" == strMongosslKeyPath:
                LOG().error("fail create mongodb connector, no ssl key path")
                sys.exit(1) #이건 종료.


            mongodbClient = pymongo.MongoClient(strMongoDBURL
                , ssl=True
                , ssl_certfile=strMongosslKeyPath
                #, ssl_cert_reqs=ssl.CERT_REQUIRED,
                , ssl_cert_reqs=ssl.CERT_NONE
                #, ssl_ca_certs='~/ssl/ca.pem'
                , unicode_decode_error_handler='ignore'
            )
        else:

            mongodbClient = pymongo.MongoClient(strMongoDBURL
                , unicode_decode_error_handler='ignore'
            )

        return mongodbClient



    #SSL Client 반환
    #TODO: IPv6 는 strIP 에서 처리.
    def GetMongoSSLClient(self, strIP, nPort, strCertFile):

        LOG().info("create mongo ssl client, {}:{}/{}".format(strIP, nPort, strCertFile))

        #ssl_cert_reqs=ssl.CERT_REQUIRED 를 사용시 인증서 오류 발생함.
        #SSL handshake failed: 10.0.13.157:21011: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed

        mongodbClient = pymongo.MongoClient(strIP
            , nPort
            , ssl=True
            , ssl_certfile=strCertFile
            #, ssl_cert_reqs=ssl.CERT_REQUIRED,
            , ssl_cert_reqs=ssl.CERT_NONE
            #, ssl_ca_certs='~/ssl/ca.pem'
            , unicode_decode_error_handler='ignore'
            )

        return mongodbClient

    #일반 Client 반환
    def GetMongoClient(self, strIP, nPort):

        LOG().info("create mongo plain client {}:{}".format(strIP, nPort))

        #https://stackoverflow.com/questions/36314776/pymongo-error-bson-errors-invalidbson-utf8-codec-cant-decode-byte-0xa1-in-p
        mongodbClient = pymongo.MongoClient(strIP, nPort, unicode_decode_error_handler='ignore') 
        return mongodbClient

    # #ip, pw 인증 추가
    # def SetAuthentication(self, mongodbClient, strMongoAuthID, strMongoAuthPassword):

    #     mongodbClient.admin.authenticate(strMongoAuthID, strMongoAuthPassword)
    #     return ERR_OK

    
    
