#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import commands
import os
import time

VOICE_OUT_PATH = '/home/pi/tmp.wav'

M_FORWARD = '#M1'
M_BACK = '#M2'
M_RIGHT = '#M3'
M_LEFT = '#M4'
    
msgs = ['はい、後ろに...','まわり','左に','前に進む']

def speak(message):
    print('speaking...' + message)
    JDIC_DIR='/var/lib/mecab/dic/open-jtalk/naist-jdic/'
    VOICE_DATA='/home/pi/ai/mei/mei_happy.htsvoice'
    
    cmdline = 'echo ' + message + ' | open_jtalk -x ' + JDIC_DIR + \
        ' -m ' + VOICE_DATA + ' -ow ' + VOICE_OUT_PATH + \
        ' -s 17000 -p 100 -a 0.03'
    print(commands.getoutput(cmdline))    
    os.system('play ' + VOICE_OUT_PATH)
    
def robot(message):   
    if ('前に' in message):
        ser.write(M_FORWARD)         
        speak('はい、前にきます。')
    elif ('後ろに' in message):
        ser.write(M_BACK)         
        speak('はい、後ろにいきます。')
    elif ('右に' in message):
        ser.write(M_RIGHT)         
        speak('はい、右手あげます。')
    elif ('左に' in message):
        ser.write(M_LEFT)         
        speak('はい、左手あげます。')
    else:
        return False
    return True

if __name__ == '__main__':
    #open serial port
    os.system('sudo chmod 777 /dev/ttyAMA0')      
    ser = serial.Serial('/dev/ttyAMA0', 38400)

    for msg in msgs:
        print('message:' + msg)
        did=robot(msg)
        if (not did):
            speak(msg + 'はよく分かりません。')
        time.sleep(1)
