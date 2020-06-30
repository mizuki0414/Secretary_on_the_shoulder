#!/usr/bin/env python
# coding: UTF-8
import os
import commands
import time

VOICE_OUT_PATH = '/home/pi/tmp.wav'

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
    message = 'こんにちは'
    t0 = current_milli_time()
    speak(message)
    print 'speaked:' + str(current_milli_time() - t0) + 'ms'
    
