#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import smtplib
import datetime
import traceback #try/except

from email.mime.text import MIMEText  # 본문 내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart   # 메시지를 보낼 때 메시지에 대한 모듈
from email import utils #날짜 관련

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#외부 라이브러리 선언
#logger
from libutil.logger import *
from libjson.json_helper import JsonHelper #json helper
from libglobal.global_const import * #전역상수

from libconv.py_conv import * #python2,3 호환 (대개는 인코딩 문제)

#TODO: 메인 프로세스의 실행 위치에 따라 경로가 달라져서, 외부 경로로 접근하는게 낫다.
from libmail.mail_style_text_convertor import MailStyleTextConvertor #메일 테스트 변환 모듈

'''
메일발송 모듈
재사용이 필요한 사항
메일 주소, 포트, 송신자 => 재사용을 하지 않음.
TODO: 대량 메일 발송이 필요할경우, 별도의 데몬 모듈 개발
'''
class SMTPMailSender:

    '''
    def __init__(self):
        # 공통적으로 사용할 클래스 변수 (제거하고 싶지만, 내버려 둠)
        #self.__strMailURL = None #메일 발송 주소
        #self.__nMailPort = None #메일 발송 포트
        pass
    '''

    #script 파일을 열어서, 메일 발송
    def SendMailByScript(self, strScriptPath):

        #file을 map으로 변환
        #예외처리는 나중
        dictMailScript = {}

        #인자의 file을 dict로 변환
        JsonHelper.JsonFileToDictionary(strScriptPath, dictMailScript)
        self.SendMailByDict(dictMailScript)

        return ERR_OK

    #dataMap으로 파일 전송
    def SendMailByDict(self, dictMailScript):

        #여기서부터는, 정해진 규칙
        dataMap = dictMailScript.get("data_map")
        strStyleFilePath = dictMailScript.get("style_file")
        dictResult = {} #변환결과 문자열

        #script의 내용중 style 파일과 datamap을 변환가공
        sytyleConvertor = MailStyleTextConvertor()
        sytyleConvertor.DoProcStyleFile(strStyleFilePath, dataMap, dictResult)

        #보낼 데이터
        txtMailContents = dictResult.get("contents") #반드시 있어야 함.

        mailURL = dictMailScript.get("mail_url")
        mailPort = dictMailScript.get("mail_port")
        fromMail = dictMailScript.get("from_mail")
        lstRecvMail = dictMailScript.get("recv_mail_list")
        mailSubject = dictMailScript.get("subject")

        lstAttachFile = dictMailScript.get("attach_file") #파일첨부 (파일 경로)

        self.SendSimpleTextMail(mailURL, mailPort, fromMail, lstRecvMail, mailSubject, txtMailContents, lstAttachFile)

        return ERR_OK


    #단순 메일 발송
    #각 메일은 독립적으로 건건이 발송
    #url, port 도 저장하지 않는다, 건건이 발송.
    #정말 단순, 포워드. TODO: 향후 확장을 위해서는 dictionary로 단순화 하는 것도 방법
    #수신자는 다수 지원하도록 설정
    def SendSimpleTextMail(self, mailURL, mailPort, fromMail, lstRecvMail, mailSubject, txtMailContents, lstAttachFile):

        #strMailURL = self.__strMailURL #메일 주소
        #nMailPort = self.__nMailPort #메일 포트

        #TODO: python2 에서 문자열 에러 발생
        #UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
        #기능이면 잡겠는데, 우선 로그라서, 제거
        '''
        LOG().debug("send mail, url={}, port={}, from={}, to-list={}, subject={}".format(
            mailURL, mailPort, fromMail, lstRecvMail, mailSubject
        ))
        '''

        #예외가 발생해도, 다음 처리를 수행

        #TODO: 다수의 메일발송이나 성능이 필요할경우 statefull 패턴으로 개발
        #여기 개선 검토

        #TODO: 접속 에러가 날수 있는데, 이부분에 대한 예외처리 필요
        #전체 에러를 잡는다.
        try:

            #향후 보안 인증도 검토
            #https://s-engineer.tistory.com/234
            #s = smtplib.SMTP('smtp.gmail.com', 587)
            #s.starttls()
            #s.login('위의 세팅된 gmail계정', '위의 16글자 비밀번호')

            #strMailID = "acf21s9@gmail.com"
            #strMailPW = "dxmtqtsunveazrxz"

            # strMailServer = "smtp.gmail.com"
            # nMailPort = 587

            smtp = smtplib.SMTP(mailURL, mailPort)

            smtp.ehlo()

            for recvToMail in lstRecvMail:

                try:

                    LOG().info("메일 발송, 수신자={}".format(recvToMail))

                    if None != lstAttachFile:
                        self.__SendMultiPartSMTPMail(smtp, fromMail, recvToMail, mailSubject, txtMailContents, lstAttachFile)
                    else: #TODO: 기존코드와의 호환성, 향후 제거
                        self.__SendSimpleSMTPMail(smtp, fromMail, recvToMail, mailSubject, txtMailContents)

                except Exception as err:
                    LOG().error(err)
                    LOG().error(traceback.format_exc())
                    LOG().error("메일 전송 실패 메일주소 = {}".format(recvToMail))
                    continue

            smtp.quit()

        except Exception as err:

            LOG().error(traceback.format_exc())
            LOG().error("메일 전송 오류 url= {}, port = {}".format(mailURL, mailPort))
            return ERR_FAIL

        return ERR_OK

    ################################################ private

    #단순 메일 전송 예제
    def __SendSimpleSMTPMail(self, smtp, fromMail, toMail, mailSubject, mailContents):
        #https://medium.com/@mika94322/python-smtp-email-%EC%A0%84%EC%86%A1-%EC%98%88%EC%A0%9C-c7e6e095dcfc

        #utf-8로 변환 (python2 오류)
        mailContents = PYCONV().UTF8Text(mailContents)

        msg = MIMEText(mailContents, _charset="UTF-8") 

        #msg['Subject'] = Header(strMailSubject,"utf-8"), mail header, 추가 가능
        msg['Subject'] = mailSubject #메일 제목

        #TODO: 계정이 두번 들어가는데 => 들어가야함 (메일 제목에 안나옴)
        msg['From'] = fromMail #송신자
        msg['To'] = toMail #수신자
        msg['cc'] = "acf21@gmail.com" #TODO: 리펙토링, CC추가
        #숨은 참조, TODO: 향후 추가
        #msg['bcc'] = "acf21@gmail.com"

        #출처: https://del4u.tistory.com/128 [창조적 귀차니즘]
        msg['Date'] = utils.formatdate(localtime = 1)

        smtp.sendmail(fromMail, toMail, msg.as_string())
        
        return ERR_OK

    #파일 첨부 메일, 중복인데, 사실상 msg 타입이 달라져서, 분리 
    def __SendMultiPartSMTPMail(self, smtp, fromMail, toMail, mailSubject, mailContents, lstFileInfo):

        #제목, 본문
        msg = MIMEMultipart()

        msg['Subject'] = mailSubject
        #msg.attach(MIMEText(mailContents, 'plain'))

        msgContents = MIMEText(mailContents, _charset="UTF-8")
        msg.attach(msgContents)

        msg['Date'] = utils.formatdate(localtime = 1)
        msg['From'] = fromMail #송신자
        msg['To'] = toMail #수신자

        # 파일첨부 (파일 미첨부시 생략가능)
        if None != lstFileInfo:

            for strFileFullPath in lstFileInfo:

                strAttachFileName = os.path.basename(strFileFullPath) #첨부파일명

                part = MIMEBase('application', 'octet-stream')             

                attachment = open(strFileFullPath, 'rb')   
                part.set_payload((attachment).read())
                encoders.encode_base64(part)

                part.add_header('Content-Disposition', "attachment; filename= " + strAttachFileName)
                msg.attach(part) #TODO: N개가 되는지 확인

        smtp.sendmail(fromMail, toMail, msg.as_string())
        
        return ERR_OK



