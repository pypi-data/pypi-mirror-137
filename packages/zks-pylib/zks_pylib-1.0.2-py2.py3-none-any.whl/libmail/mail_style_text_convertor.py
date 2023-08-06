#!/usr/bin/python
# -*- coding: utf-8 -*-

#외부 라이브러리 선언
#logger
from libutil.logger import *
from libutil.file_io_helper import FileIOHelper #file 객체 관리
from libglobal.global_const import * #전역상수


'''
메일 style convertor
style 과 데이터를 병합후, 결과를 txt로 생성한다.
style은 html이 될수도 있고, 데이터가 될수도 있다. 
병합을 관리한다.
'''

class MailStyleTextConvertor:

    def __init__(self):
        # 공통적으로 사용할 클래스 변수 (제거하고 싶지만, 내버려 둠)        
        pass


    #초기화 로직, 아마도 경로가 될듯
    #아니다, 상태가 없어야 한다. style 파일은 매번 인자로 받는다.
    #필요없으면 제거
    '''
    def Initialize(self):

        pass
    '''

    #config로 변환할수 있도록 구성한다. => script로 명명
    #def DoProcyMailScript

    #File 형태의 style 파일을 변환한다.
    #style파일은 파일로 열고, 다시 DoProcStyleTextMessage를 호출
    #다만 dataMap은 좀 길더라도 map이 낫다고 봄, 향후 file로 관리하려면 json 파일로 관리
    def DoProcStyleFile(self, strStyleFilePath, dataMap, dictResult):

        LOG().debug("do process style file")
        
        styleMessage = FileIOHelper.OpenFileAsUTFToStream(strStyleFilePath)

        if None == styleMessage:
            LOG().error("Fail Open Style File, skip")
            return ERR_FAIL

        self.DoProcStyleTextMessage(styleMessage, dataMap, dictResult)

        return ERR_OK

    #Text메시지 형태의 가공
    def DoProcStyleTextMessage(self, styleMessage, dataMap, dictResult):

        LOG().debug("do process style text message")

        #dataMap의 key에 ##을 추가해서, styleMessage에 존재하는 key를 value로 변환한다.

        #메시지는, 원본은 내버려 두고, 새로 만들자.
        #TODO: Key에 ##을 추가하는 것으로 하자. 필요에 따라서는 # 뿐만 아니라 $ % 등도 되도록.
        strFullStyleMsg = styleMessage #우선 복사

        for key in dataMap:

            value = dataMap.get(key)

            if None == value:
                LOG().error("invalid key {} (not exist)".format(key))
                return ERR_FAIL #하나라도 실패하면, FAIL 이다.

            strFullStyleMsg = strFullStyleMsg.replace(key, value)

        #TODO: 결과를, dict 로반환하는 것을 생활화.
        #굳이 별도로 선언하지 말고, 키만 맞춘다.
        dictResult["contents"] = strFullStyleMsg
        dictResult["code"] = ERR_OK

        return ERR_OK