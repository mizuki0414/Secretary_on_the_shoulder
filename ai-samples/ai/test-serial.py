#!/usr/bin/env python
# coding: UTF-8
import os
import serial
import time

#open serial port
os.system('sudo chmod 777 /dev/ttyAMA0')  
ser = serial.Serial('/dev/ttyAMA0', 57600)
i = 0

try:
    while True:
        message = 'Test' + str(i)
        print('TX:' + message)
        ser.write(message + '\r\n')
        i = i + 1
        time.sleep(1)            

except KeyboardInterrupt:
    pass

ser.close()


