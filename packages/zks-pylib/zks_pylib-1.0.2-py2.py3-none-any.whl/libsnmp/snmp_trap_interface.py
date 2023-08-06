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

import concurrent.futures
import re
import json

#snmp 관련
from pysnmp.hlapi import *
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp, udp6
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from pysnmp.smi import builder, view, compiler, rfc1902, error
from multiprocessing import Queue

class SnmpTrapInterface:
    def __init__(self):
        self.put_count = 0
        self.snmpEngine = SnmpEngine() 
        self.contextData = ContextData() 

        self.queue = Queue()

        pass

    def DoTrapNameToMatch(self, name, snmpResult, rePattern, dictLog):  

        try:
            if len(rePattern) > 0 and len(snmpResult) > 0:

                match = re.search(rePattern, snmpResult)
                result = match.groupdict()
                if len(result) > 0:

                    # pattern 탐지 결과가 여러개 일 경우
                    # nic 번호, port 번호를 차례로 작성하며, ','를 넣어준다.
                    nic = result.get('nic')
                    port = result.get('port')

                    sResult = "{0}{1}".format(nic, port)
                    dictLog[name] = sResult

                else:
                    LOG().error("No Pattern Data")
            else:
                LOG().error("Pattern : {0}, Result : {1}".format( rePattern, snmpResult))

        except Exception:
            LOG().error(traceback.format_exc())


    #실제 수행 Worker
    def DoTrapSnmp(self, dicSnmpTrapInfo):

        transportDispatcher = None

        try:
            #snmp_version = dicSnmpworker.get("snmp_version")
            nTmsSnmpVersion = int(dicSnmpTrapInfo.get("TMS_SNMP_VERSION"))
            nTmsSnmpListenPort = int(dicSnmpTrapInfo.get("TMS_SNMP_LISTEN_PORT"))
            nTmsSnmpIpVersion = int(dicSnmpTrapInfo.get("TMS_SNMP_IP_VERSION"))
            sTmsSnmpCommunity = dicSnmpTrapInfo.get("TMS_SNMP_COMMUNITY")

            if nTmsSnmpVersion == 3:
                #    add_snmp_v3(snmpEngine) # snmp version 3
                self.__DoAddSnmpv3(self.snmpEngine, sTmsSnmpCommunity)
            else:
                #add_snmp_v2(snmpEngine) # snmp version 1, 2
                self.__DoAddSnmpv2(self.snmpEngine, sTmsSnmpCommunity)

            # NotificationReceiver accepting messages with CommunityName’s
            # ntfrcv.NotificationReceiver(snmpEngine, self.cbFun)

            # dictExtOpt 의 값들을 사용하여 값 셋팅 작업 필요
            #

            self.__Add_TransPort(self.snmpEngine, nTmsSnmpListenPort, nTmsSnmpIpVersion) # port, iptype(4:ipv4,6:ipv6)

            # 스레드 사용 안함
            ntfrcv.NotificationReceiver(self.snmpEngine, self.__DoCbRecv)

            # Register an imaginary never-ending job to keep I/O dispatcher running forever
            # 이 함수에서 대기하게 됨
            transportDispatcher = self.snmpEngine.transportDispatcher

            if None != transportDispatcher:

                transportDispatcher.jobStarted(1)

                # Run I/O dispatcher which would receive queries and send responses
                transportDispatcher.runDispatcher()


            ################################################################################################################

        except Exception:
            # 종료 수행

            LOG().error(traceback.format_exc())

            sys.exit(-1) #여기서 에러는 강제 종료

            if None != transportDispatcher:
                transportDispatcher.closeDispatcher()

    def GetAllTraps(self):
        traps_list = []
        while not self.queue.empty():
            traps_list.append(self.queue.get())

        return traps_list


    def __Add_TransPort(self, snmpEngine, nTmsSnmpListenPort, nTmsSnmpIpVersion):

        #snmp_trap_port = dicSnmpworker.get("snmp_trap_port")
        #snmp_iptype = dicSnmpworker.get("snmp_iptype")

        if nTmsSnmpIpVersion == 6:
            config.addTransport(
                            snmpEngine,
                            udp.domainName,
                            udp6.Udp6SocketTransport().openServerMode(('::', nTmsSnmpListenPort))
                            )
        else:
            config.addTransport(
                            snmpEngine,
                            udp.domainName,
                            udp.UdpTransport().openServerMode(('0.0.0.0',nTmsSnmpListenPort))
                            )

        #LOG().error("%d Port Binding Failed the Provided Port %s is in Use" , snmp_trap_port, str(e))

    def __DoCbRecv(self, snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):

        execContext = snmpEngine.observer.getExecutionContext('rfc3412.receiveMessage:request')
        data = {}
        data['transportAddress'] = execContext['transportAddress'][0]
        data['varBinds'] = varBinds

        self.put_count += 1
        self.queue.put(data)
        
        #LOG().debug("[Queue Put Index : {0}]".format(self.put_count))

    def __DoAddSnmpv2(self, snmpEngine, sTmsSnmpCommunity):

        #snmp_community = dicSnmpworker.get("snmp_community")

        config.addV1System(snmpEngine, sTmsSnmpCommunity, sTmsSnmpCommunity) # Community 이름 추가
        #config.addV1System(snmpEngine, 'public1', 'public1')  # Community가 더 있을 경우 추가
        #config.addV1System(snmpEngine, 'public2', 'public2')  # Community가 더 있을 경우 추가

    def __DoAddSnmpv3(self, snmpEngine, sTmsSnmpCommunity):
        #  나중에 테스트 필요

        #snmp_community = dicSnmpworker.get("snmp_community")

        # V3 User가 여러개일 경우 아래를 User 개수 만큼 수행한다.
        # snmp v3는 나중에 테스트 한다.
        __authProtocol = {'usmHMACMD5AuthProtocol': config.usmHMACMD5AuthProtocol,'usmHMACSHAAuthProtocol': config.usmHMACSHAAuthProtocol,'usmAesCfb128Protocol': config.usmAesCfb128Protocol,'usmAesCfb256Protocol': config.usmAesCfb256Protocol,'usmAesCfb192Protocol': config.usmAesCfb192Protocol,'usmDESPrivProtocol': config.usmDESPrivProtocol,'usmNoAuthProtocol': config.usmNoAuthProtocol,'usmNoPrivProtocol': config.usmNoPrivProtocol}
        v3_user = '' # Provide V3 User Name
        v3_authkey = '' # Provide Auth Key
        v3_privkey = '' # Provide Priv Key
        authProtocol = '' # Provide authProtocol: Option: [usmNoAuthProtocol, usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol]
        privProtocol = ''# Provide privProtocol: Option: [usmNoPrivProtocol, usmDESPrivProtocol, usm3DESEDEPrivProtocol, usmAesCfb128Protocol]
        securityEngineId = '' #Provide V3 security EngineId e.g. 800000d30300000e112245
        config.addV3User( snmpEngine, userName=v3_user, authKey=v3_authkey, privKey=v3_privkey, authProtocol=__authProtocol.get(authProtocol, config.usmNoAuthProtocol), privProtocol=__authProtocol.get(privProtocol,config.usmNoPrivProtocol),securityEngineId=v2c.OctetString(hexValue=securityEngineId))