#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os #디렉토리 관리

import speech_recognition as sr 
from gtts import gTTS
import playsound


'''
tts 모듈 실행
'''
def DoPlayTTS(txtMessage, _lang='ko', filename="voice.mp3", bRemove=True):

    tts = gTTS(text=txtMessage, lang=_lang) 
    
    tts.save(filename) 

    playsound.playsound(filename)

    if True == bRemove:
        os.remove(filename)


    return 0