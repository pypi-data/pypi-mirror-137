#!/usr/bin/python
# -*- coding: utf-8 -*-

import traceback
import time 
#snmp 관련
import threading
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp

from pysnmp.entity.rfc3413 import ntforg

#외부 라이브러리 import
from libutil.logger import *
from libglobal.global_const import *

class SnmpSendInterface:

    def __init__(self):

        self.snmpEngine = engine.SnmpEngine()
        #self.contextData = ContextData() 

        #self.ntfOrg = None

        pass

    def Initialize(self, nIndex, nSnmpJobWaitSec, sSnmpServerIP, nSnmpSendPort, sSnmpCommunity):

        config.addV1System(self.snmpEngine, 'my-area', sSnmpCommunity, transportTag='all-my-managers')

        config.addTargetParams(self.snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 0)

        # Setup transport endpoint and bind it with security settings yielding
        # a target name
        config.addTransport(
            self.snmpEngine,
            udp.domainName,
            udp.UdpSocketTransport().openClientMode()
        )

        config.addTargetAddr(
            self.snmpEngine, 'my-nms',
            udp.domainName, (sSnmpServerIP, nSnmpSendPort),
            'my-creds',
            tagList='all-my-managers'
        )

        # Specify what kind of notification should be sent (TRAP or INFORM),
        # to what targets (chosen by tag) and what filter should apply to
        # the set of targets (selected by tag)
        config.addNotificationTarget(
            self.snmpEngine, 'my-notification', 'my-filter', 'all-my-managers', 'trap'
        )

        # Allow NOTIFY access to Agent's MIB by this SNMP model (1), securityLevel
        # and SecurityName
        config.addContext(self.snmpEngine, '')
        config.addVacmUser(self.snmpEngine, 1, 'my-area', 'noAuthNoPriv', (), (), (1, 3, 6))


        self.ntfOrg = ntforg.NotificationOriginator()

        threading.Thread(target=self.ThreadHandlerProc, args=(nIndex, nSnmpJobWaitSec)).start()


    # Error/response receiver
    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def cbSendSnmp(self, snmpEngine, sendRequestHandle, errorIndication,
            errorStatus, errorIndex, varBinds, cbCtx):
        if errorIndication:
            LOG().error("Send Snmp Error : {0}".format(errorIndication))
        elif errorStatus:
            LOG().error("Send Snmp Error : {0} at {1}".format(errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))


    def ThreadHandlerProc(self, nIndex, nSnmpJobWaitSec):    

        while True:
        
            tStime = time.time()
            transportDispatcher = self.snmpEngine.transportDispatcher

            if None != transportDispatcher:

                transportDispatcher.jobStarted(1)
                LOG().info("runDispatcher Start Index : {0}, Pid : {1}".format(nIndex, os.getpid()))
                # Run I/O dispatcher which would receive queries and send responses
                transportDispatcher.runDispatcher()
                LOG().info("runDispatcher End Index : {0}, Pid : {1}".format(nIndex, os.getpid()))

            
            time.sleep(nSnmpJobWaitSec)
                
    def DoSnmpTrapSend(self, lstTrapData):

        # Create Notification Originator App instance. 
        
        self.ntfOrg.sendVarBinds(
            self.snmpEngine,
            # Notification targets
            'my-notification',  # notification targets
            None, '',  # contextEngineId, contextName
            # var-binds
            lstTrapData,
            self.cbSendSnmp
        )

