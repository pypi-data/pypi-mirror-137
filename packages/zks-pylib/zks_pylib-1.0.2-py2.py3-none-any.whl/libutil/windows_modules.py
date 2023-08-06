#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import psutil #프로세스 종료
import traceback

from libutil.logger import *

'''
Windows system 용 모듈
우선 함수 (사용여부는 모르겠다.) 리펙토링도 필요
'''

#프로세스 종료
def KillProcess(sFindKey):

    #에러가 발생하면, 무시하고 다음 작업.
    try:

        #path 강제 추가 (taskkill이 안먹히는 경우 존재)
        os.environ["PATH"] += os.pathsep + os.pathsep.join(["%windir%\\System32;%Path%"])

        for process in psutil.process_iter():
            # check whether the process name matches

            #열린 파일 경로 가져오기
            #https://klonic.tistory.com/88
            #process.pid 
            #process.name
            #process.started

            LOG().debug("pid={0}, process-name={1}".format(process.pid , process.name))

            pHandle = psutil.Process(process.pid)

            lstCmdLine = pHandle.as_dict().get("cmdline")
            sCWD = pHandle.as_dict().get("cwd")

            if None == lstCmdLine: #없는 경우가 존재한다.
                continue

            for cmdLine in lstCmdLine:
                if 0 <= cmdLine.find(sFindKey):
                    LOG().info("kill proess pid={0}, cwd={1}, cmdline={2}".format(process.pid, sCWD, lstCmdLine))
                    #process.kill()
                    #os.kill(process.pid, SIGKILL)
                    os.system("C:\\Windows\\System32\\taskkill /f /pid  {0}".format(process.pid))

    except Exception as err:
    #except getopt.GetoptError as err:

        LOG().error(str(err))
        LOG().error(traceback.format_exc())
        #sys.exit(PROCESS_EXIT_CODE_SUCCESS)
        pass

    pass #TODO: 반환값 어떻게?
