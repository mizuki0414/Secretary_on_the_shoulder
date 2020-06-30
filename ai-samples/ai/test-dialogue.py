#!/usr/bin/env python
# coding: UTF-8
import requests
import json
import time

DOCOMO_APIKEY = 'Input your docomo key here.'

def dialogue(messageg):
    print('dialoguing...>>' + message)
    url = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}'.format(DOCOMO_APIKEY)
    payload = {'utt': message}
    
    try: 
        r = requests.post(url, data=json.dumps(payload))
    except:
        return '#ERROR'
    return r.json()['utt'].encode('utf-8')

def current_milli_time():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    message = 'こんにちは'
    t0 = current_milli_time()
    reply = dialogue(message)
    print '<<:' + reply
    print 'replied:' + str(current_milli_time() - t0) + 'ms'
