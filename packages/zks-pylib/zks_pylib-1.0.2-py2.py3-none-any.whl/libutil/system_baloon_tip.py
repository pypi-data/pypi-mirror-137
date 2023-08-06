
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time


#외부 라이브러리
from libutil.logger import *
from libglobal.global_const import *

class WindowsBalloonTip:

    def __init__(self, title, msg):

        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "TMS plus"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        
        #icon => 현재 경로로. (향후 config)

        #strIconPath = "../resources/icon/TMSPlus.ico"

        #LOG().info(os.path.abspath(__file__))

        strCurrentPath = os.path.dirname(os.path.realpath(__file__))

        strIconPath = "{}/../resources/icon/TMSPlus.ico".format(strCurrentPath)

        #iconPathName = os.path.abspath(os.path.join( sys.path[0], "TMSPlus.ico" ))
        #strIconPath = os.path.abspath(os.path.abspath(__file__), "TMSPlus.ico" )
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        
        try:
            hicon = LoadImage(hinst, strIconPath, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
            LOG().error("No Icon, path = {}".format(strIconPath))
        
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(1)
        #DestroyWindow(self.hwnd)

        #ShowWindow(self.hwnd, win32con.SW_HIDE)

        #nid = (self.hwnd, 0)
        #Shell_NotifyIcon(NIM_DELETE, nid)

        PostQuitMessage(0) # Terminate the app.
        

        #TODO: 향후 클릭 이벤트 => 일단 밖에서 호출후 shell 호출
    
    def OnDestroy(self, hwnd, msg, wparam, lparam):

        LOG().debug("destroy window")

        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
        pass
    
'''
def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)

if __name__ == '__main__':
    balloon_tip("TMS plus 장애 알람", "NIC 다운 장애 알람2")

'''