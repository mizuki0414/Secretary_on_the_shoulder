#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import os
import time

GOOGLE_APIKEY = 'input your Google key here.'
VOICE_REC_PATH = '/home/pi/ai/hello.flac'

def recognize():
    print('recognizing...')
    f = open(VOICE_REC_PATH, 'rb')
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

def current_milli_time():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    t0 = current_milli_time()              
    message = recognize().encode('utf-8')
    print 'recognized:' + str(current_milli_time() - t0) + 'ms'
    if (message == '#CONN_ERR'):
        print 'internet not available'
        message = ''         
    elif (message == '#ERROR'):
        print 'voice recognizing failed'                
        message = ''          
    else:
        print 'your words:' + message
