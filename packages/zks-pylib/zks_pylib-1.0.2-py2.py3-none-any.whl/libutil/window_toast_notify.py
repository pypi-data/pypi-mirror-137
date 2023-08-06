#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os #디렉토리 관리
import time

from win10toast import ToastNotifier
from plyer import notification
#from src.win10toast.win10toast import ToastNotifier 


'''
Windows 10 toast Notify 실행
pyler, windows10 toast 둘중 하나 선택
단독으로 선택 + python 3만 검토
'''
def DoNotifyWindowToast(_title, _message):

    toaster = ToastNotifier()
    #toaster.show_toast(_title , _message, duration = _duration, threaded=True)
    toaster.show_toast(_title , _message, threaded=True)

    #callback 대신, toast와 click 메소드 같이 실행
    #time.sleep(1)
    #CallShellCommand(shellCommand)

    return 0

'''
pyler 를 이용한 notify
'''
#def DoNotifyPlyerToast(_title, _message, _appName, _timeout, shellCommand=None):
def DoNotifyPlyerToast(_title, _message, _appName, _timeout):

    notification.notify(
        title = _title,
        message = _message,
        app_name = _appName,
        #app_icon = 'bluemen_white.ico', # 'C:\\icon_32x32.ico'
        timeout = _timeout,  # seconds
    )

    #callback 대신, toast와 click 메소드 같이 실행
    #CallShellCommand(shellCommand)

    return 0

'''
toast 에 click 이벤트 추가
'''
def DoNotifyToastCallback(_title, _message):

    toaster = ToastNotifier()
    toaster.show_toast(_title, _message, threaded=True, callback_on_click=onClickToast)

    return 0


def onClickToast():
    os.system("notepad.exe")
    pass




if __name__ == "__main__":
   
    #main()
    pass
