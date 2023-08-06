#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import traceback
import time

#외부 라이브러리 import
from libutil.logger import *
from libglobal.global_const import *
from libsnmp.snmp_define import * #define
from pysnmp.proto.rfc1905 import endOfMibView

import concurrent.futures

#snmp 관련
from pysnmp.hlapi import *

import re
import json


class SnmpGetInterface:
    def __init__(self):

        self.snmpEngine = SnmpEngine() 
        self.contextData = ContextData() 

        pass

    def DoGetNameToMatch(self, snmpResult, rePattern, dictLog):

        try:
            if len(rePattern) > 0 and len(snmpResult) > 0:
                match = re.search(rePattern, snmpResult)
                if match:
                    result = match.groupdict()

                    if len(result) > 0:
                        for key, value in result.items():
                            dictLog[key] = value
                    else:
                        LOG().error("No Pattern Data")
                else:
                    LOG().error("No Match Data")
            else:
                LOG().error("Pattern : {0}, Result : {1}".format( rePattern, snmpResult))

        except Exception as e: #에러 처리 필요
            LOG().error("Get Match : {0}, Result : {1}".format( rePattern, snmpResult))
            LOG().error(traceback.format_exc())

        return snmpResult

    def DoBulkNameToMatch(self, snmpResult, name, rePattern, dictLog):

        strResult = ""
        if len(rePattern) > 0:
            # 패턴이 있을 경우 패턴매칭 수행하는 함수 호출
            strResult = self.__DoBulkNameToPatternMatch(name, snmpResult, rePattern, dictLog)
        else:
            # 패턴이 없을 경우 패턴매칭 수행하지 않는 함수 호출
            strResult = self.__DoBulkName(name, snmpResult, dictLog)

        return strResult

    def DoGetCommandSnmp(self, dictExtOpt, dictResult):
        try:
            #errindication (str) – True value indicates local SNMP error.
            #errstatus (str) – True value indicates SNMP PDU error reported by remote.
            #errindex (int) – Non-zero value refers to varBinds[errorIndex-1]
            #resultable (tuple) – A sequence of ObjectType class instances representing MIB variables returned in SNMP response.

            community = dictExtOpt.get(SNMP_DEF.OPT_COMMUNITY)
            port = dictExtOpt.get(SNMP_DEF.OPT_PORT)

            ipaddr = dictExtOpt.get(SNMP_DEF.OPT_IPADDR)
            time_out = dictExtOpt.get(SNMP_DEF.OPT_TIMEOUT)
            retry_cnt = dictExtOpt.get(SNMP_DEF.OPT_RETRY)
            oid = dictExtOpt.get(SNMP_DEF.SNMP_OID)
            name = dictExtOpt.get(SNMP_DEF.SNMP_NAME)

            start = time.time()  # 시작 시간 저장
            lstResultGroup = list()
            errindication, errstatus, errindex, resultable = next(getCmd(
                self.snmpEngine,
                CommunityData(community),
                UdpTransportTarget((ipaddr, port), timeout=time_out, retries=retry_cnt), # timeout, retries 값 정상 동작 안함 확인 필요
                self.contextData,
                ObjectType(ObjectIdentity(oid))
                )) # snmp get 수행

            if errindication:
                #dictResult[name] = str(errindication) # 에러 발생시 결과값에 저장
                LOG().error("Get Snmp Error ip = {0} name = {1} oid = {2} err = {3} time = {4}s timeout = {5} retry = {6} community = {7} port = {8}".format(ipaddr, name, oid, str(errindication), time.time() - start, time_out, retry_cnt, community, port))
                return ERR_FAIL
            # 에러 처리 확인 필요
            # https://www.pythonstudio.us/system-administration/querying-snmp-devices-from-python.html
            #elif errstatus:
            #    dictResult[key] = str(errstatus)
            #    print('SNMP error: %s at %s', errstatus.prettyPrint(),
            #         errindex and restable[-1][int(errindex) - 1] or '?')
            else:
                for oid, val in resultable:
                    dictResult[SNMP_DEF.RES_DATA] = val.prettyPrint() #수신 데이터

            return  ERR_OK #에러코드
        except Exception as e:
            LOG().error(traceback.format_exc())
            return ERR_FAIL

    def DoBulkCommandSnmp(self, dictExtOpt, dictResult):
        try:
            #errindication (str) – True value indicates SNMP engine error.
            #errstatus (str) – True value indicates SNMP PDU error.
            #errindex (int) – Non-zero value refers to *varBinds[errorIndex-1]
            #resultable (tuple) – A sequence of ObjectType class instances representing MIB variables returned in SNMP response.

            community = dictExtOpt.get(SNMP_DEF.OPT_COMMUNITY)
            port = dictExtOpt.get(SNMP_DEF.OPT_PORT)
            ipaddr = dictExtOpt.get(SNMP_DEF.OPT_IPADDR)
            time_out = dictExtOpt.get(SNMP_DEF.OPT_TIMEOUT)
            retry_cnt = dictExtOpt.get(SNMP_DEF.OPT_RETRY)
            oid = dictExtOpt.get(SNMP_DEF.SNMP_OID)
            #strResult = ''

            start = time.time()  # 시작 시간 저장
            lstResultGroup = list()
            for (errindication, errstatus, errindex, resultable) in bulkCmd(
                self.snmpEngine,
                CommunityData(community),
                UdpTransportTarget((ipaddr, port), timeout=time_out, retries=retry_cnt), # timeout, retries 값 정상 동작 안함 확인 필요
                self.contextData,
                0, # nonRepeaters (int) – One MIB variable is requested in response for the first nonRepeaters MIB variables in request.
                2, # maxRepetitions (int) – maxRepetitions MIB variables are requested in response for each of the remaining MIB variables in the request
                            # (e.g. excluding nonRepeaters). Remote SNMP engine may choose lesser value than requested.
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode =False):

                if errindication:
                    #LOG().error("Bulk Snmp Error ip = {0} oid = {1} err = {2}".format(ipaddr, oid, str(errindication)))
                    LOG().error("Bulk Snmp Error ip = {0} oid = {1} err = {2} time = {3}s timeout = {4} retry = {5}".format(ipaddr, oid, str(errindication), time.time() - start, time_out, retry_cnt))
                    return ERR_FAIL
        
                #elif errstatus:
                #    LOG().info("Error Status {0} at {1} ".format(errstatus.prettyPrint(), errindex and varBinds[int(errindex)-1][0] or '?' ))
                #    break
                else:
                    
                    for varBind in resultable:
                        name, val = varBind
                        if val != endOfMibView:

                            lstResultGroup.append(val.prettyPrint())

                    dictResult[SNMP_DEF.RES_DATA] = lstResultGroup

    
            return  ERR_OK #에러코드

        except Exception as e:
            LOG().error(traceback.format_exc())
            return ERR_FAIL

    # 패턴이 있을 경우 패턴매칭 수행하는 함수
    def __DoBulkNameToPatternMatch(self, name, snmpResult, rePattern, dictLog):
        try:
            lstlinkstatus = []
            for strData in snmpResult:     # 수집 결과를 List에서 꺼낸다.
                if len(rePattern) > 0 and len(strData) > 0:
                    match = re.search(rePattern, strData)
                    if match:
                        result = match.groupdict()
                        if len(result) > 0:

                            # pattern 탐지 결과가 여러개 일 경우
                            pos = int(result.get('nic')) * 2 + int(result.get('port'))
                            if result.get('status') == 'down':
                                lstlinkstatus.insert(pos, '0')
                            elif result.get('status') == 'up':
                                lstlinkstatus.insert(pos, '1')
                            else:
                                LOG().error("UnKnown Status")
                        else:
                            LOG().error("No Pattern Data")
                    else:
                        LOG().error("No Match Data")
                else:
                    LOG().error("Pattern : {0}, Result : {1}".format( rePattern, snmpResult))

            strResult = ''.join(lstlinkstatus)
            dictLog[name] = strResult

        except Exception: #에러 처리 필요

            LOG().error("Get Match : {0}, Result : {1}".format( rePattern, snmpResult))
            LOG().error(traceback.format_exc())

        return strResult

    # 패턴이 없을 경우 패턴매칭 수행하지 않는 함수
    def __DoBulkName(self, name, snmpResult, dictLog): 

        lstPoStatus = list()
        strResult = ""
        if snmpResult != None:
            
            for index in range(len(snmpResult)):
                if index == 0:
                    #lstPoStatus[0] = snmpResult[0] # 수집 결과 0번 값이 결과값 0번  port    
                    lstPoStatus.insert(index, snmpResult[index])
                elif index == 1:
                    #lstPoStatus[2] = snmpResult[1] # 수집 결과 1번 값이 결과값 2번  port                    
                    lstPoStatus.insert(index+1, snmpResult[index])
                elif index == 2:
                    #lstPoStatus[1] = snmpResult[2] # 수집 결과 2번 값이 결과값 1번  port
                    lstPoStatus.insert(index-1, snmpResult[index])
                elif index == 3:
                    #lstPoStatus[3] = snmpResult[3] # 수집 결과 3번 값이 결과값 3번  port
                    lstPoStatus.insert(index, snmpResult[index])

            strResult = ','.join(lstPoStatus) # PO 알람일 경우 , 로 묶어 준다. (향후 다른 타입이 들어올수 있으므로 별도 함수 호출 구분 필요)
            dictLog[name] = strResult

        return strResult

