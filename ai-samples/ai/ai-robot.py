#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import requests
import json
import os
import commands
import time

GOOGLE_APIKEY = 'input your Google key here.' 
DOCOMO_APIKEY = 'input your docomo key here.'
LISTEN_SECONDS = 5   
VOICE_IN_PATH = '/home/pi/tmp.flac'
VOICE_OUT_PATH = '/home/pi/tmp.wav'    

M_FORWARD = '#M1'
M_BACK = '#M2'
M_RIGHT = '#M3'
M_LEFT = '#M4'    
M_HELLO = '#M5'
M_LISTEN = '#M6'    
M_RECOG = '#M7'
M_WELL = '#M8'      
M_SPEAK = '#M9'

# 録音
def listen(seconds):
    print 'lestening...'
    cmdline = 'AUDIODEV=hw:1 rec -c 1 -r 17000 ' + VOICE_IN_PATH + \
        ' trim 0 ' + str(seconds)
    os.system(cmdline)
    return os.path.getsize(VOICE_IN_PATH)
    
# 音声認識
def recognize():
    print('recognizing...')
    f = open(VOICE_IN_PATH, 'rb')
    voice = f.read()
    f.close()

    url = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&'\
        'lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=' + GOOGLE_APIKEY
    hds = {'Content-type': 'audio/x-flac; rate=17000'}
    
    try:    
        reply = requests.post(url, data=voice, headers=hds).text
    except IOError:         
        return '#CONN_ERR'
    except:
        return '#ERROR'        
    print 'results:', reply
    
    objs = reply.split(os.linesep)
    for obj in objs:
        if not obj:
            continue
        alternatives = json.loads(obj)['result']

        if len(alternatives) == 0:
            continue
        return alternatives[0]['alternative'][0]['transcript']
    return ""             

# 対話
def dialogue(message):
    print('dialoguing...>>' + message)    
    url = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?'\
        'APIKEY={}'.format(DOCOMO_APIKEY)
    payload = {'utt': message}
    
    try: 
        r = requests.post(url, data=json.dumps(payload))
    except:
        return '#ERROR'
    return r.json()['utt'].encode('utf-8')

# 読み上げ
def speak(message):
    print('speaking...' + message)    
    JDIC_DIR='/var/lib/mecab/dic/open-jtalk/naist-jdic/'
    VOICE_DATA='/home/pi/ai/mei/mei_happy.htsvoice'
    
    cmdline = 'echo ' + message + ' | open_jtalk -x ' + JDIC_DIR + \
        ' -m ' + VOICE_DATA + ' -ow ' + VOICE_OUT_PATH + \
        ' -s 17000 -p 100 -a 0.03'
    print(commands.getoutput(cmdline))      
    os.system('play ' + VOICE_OUT_PATH)

# 音声ロボット操作
def robot(message):   
    if ('前に' in message):
        ser.write(M_FORWARD)         
        speak('はい、前にきます。')
    elif ('後ろに' in message):
        ser.write(M_BACK)         
        speak('はい、後ろにいきます。')
    elif ('右手' in message):
        ser.write(M_RIGHT)         
        speak('はい、右手あげます。')
    elif ('左手' in message):
        ser.write(M_LEFT)         
        speak('はい、左手あげます。')
    else:
        return False
    return True

def current_milli_time():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    #first time record will be failed. 
    listen(1)
    
    ser = serial.Serial('/dev/ttyAMA0', 57600)
    ser.write(M_HELLO)
    speak('こんにちは、ラズパイです。')
    
    no_word = 0
    
try:
    while True:
        # 音声入力
        t0 = current_milli_time()          
        ser.write(M_LISTEN)
        size = listen(LISTEN_SECONDS)
        t = current_milli_time() - t0
        if (t < 2000):
            print 'USB microphone not available'            
            speak('マイクロホンを確認してください。')
            time.sleep(10)
            continue
        print 'listened:' + str(t) + 'ms'
        print 'voice data size=' + str(size)
        
        # 音声認識
        ser.write(M_RECOG)
        t0 = current_milli_time()
        message = recognize().encode('utf-8')
        print 'recognized:' + str(current_milli_time() - t0) + 'ms'                          
        if (message == '#CONN_ERR'):
            print 'internet not available'
            speak('イーターネット接続を確認してください。')            
            time.sleep(10)
            continue
        elif (message == '#ERROR'):
            print 'voice recognize failed'           
            speak('音声認識サービスを確認してください。')            
            time.sleep(10)
            continue
               
        if (len(message) <= 1):
            no_word = no_word + 1
            # あいさつ             
            if (no_word >= 5):            
                ser.write(M_HELLO)
                speak('こんにちは、ラズパイです。')                
                no_word = 0             
            continue
            
        # ロボット操作
        no_word = 0 
        did = robot(message)
        if (did):
            continue
        
        # 雑談対話
        ser.write(M_WELL)
        speak('はい。')
        t0 = current_milli_time()
        reply = dialogue(message)
        print 'replied:' + str(current_milli_time() - t0) + 'ms'                
        if (reply == '#ERROR'): 
            print 'dialogue failed'
            speak('雑談会話サービスを確認してください。')            
            time.sleep(10)
            continue

        # 読み上げ
        t0 = current_milli_time()            
        ser.write(M_SPEAK)
        speak(reply)   
        print 'talked:' + str(current_milli_time() - t0) + 'ms'
        
except KeyboardInterrupt:
    pass
  
    ser.close()
