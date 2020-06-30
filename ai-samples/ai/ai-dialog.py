#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    print('dialoguing...' + message)    
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

def current_milli_time():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    #first time record will be failed. 
    listen(1)
    speak('こんにちは、ラズパイです。')    
    no_word = 0
    wifi_err = 0
    
try:
    while True:
        # 録音
        t0 = current_milli_time()          
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

        # あいさつ             
        if (len(message) <= 1):
            no_word = no_word + 1
            if (no_word >= 5):            
                speak('こんにちは、ラズパイです。')                
                no_word = 0             
            continue
               
        # 対話
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
        speak(reply)
        print 'talked:' + str(current_milli_time() - t0) + 'ms'
                  
except KeyboardInterrupt:
    pass
