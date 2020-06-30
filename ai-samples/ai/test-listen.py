#!/usr/bin/env python
# coding: UTF-8
import os
import commands
import time

LISTEN_SECONDS = 5
VOICE_IN_PATH = '/home/pi/tmp.flac'

def listen(seconds):
    print 'listening...'
    cmdline = 'AUDIODEV=hw:1 rec -c 1 -r 17000 ' + VOICE_IN_PATH + \
        ' trim 0 ' + str(seconds)
    print(commands.getoutput(cmdline))    
    return os.path.getsize(VOICE_IN_PATH)

def current_milli_time():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    t0 = current_milli_time()    
    size = listen(LISTEN_SECONDS)
    print 'recorded:' + str(current_milli_time() - t0) + 'ms'
    print 'voice data size=' + str(size)
    
    cmdline = 'play ' + VOICE_IN_PATH
    os.system(cmdline)
