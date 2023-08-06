#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


class SNMP_DEF:

    METHOD_GET = "get"
    METHOD_BULK = "bulk"

    #부가정보 필드명 (오타 방지용 상수)
    OPT_PORT = "port" #port
    OPT_IPADDR = "ip_addr" #ip주소
    OPT_COMMUNITY = 'community' #community 이름
    OPT_TIMEOUT = 'timeout'
    OPT_RETRY = 'retrycnt'
    SNMP_OID = 'oid'
    SNMP_NAME = 'name'
    SNMP_METHOD = 'method'
    RES_DATA = 'data'
  