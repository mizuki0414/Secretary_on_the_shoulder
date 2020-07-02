# -*- coding: utf-8 -*-
import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time
import pya3rt  # Talk_APIで追加

apikey = "DZZ0TIpd7cKXP0IgtSLNZQrVf7BnY8bv"  # Talk_APIキー
client = pya3rt.TalkClient(apikey)

host = "localhost"
port = 10500

p = subprocess.Popen(["./julius-start.sh"], stdout=subprocess.PIPE, shell=True)
pid = str(p.stdout.read().decode('utf-8'))  # juliusのプロセスIDを取得
time.sleep(5)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

data = ""
killword = ""

while True:

    while (1):
        if '</RECOGOUT>\n.' in data:
            # data = data + sock.recv(1024)
             strTemp = ""
             print("testest")
              for line in data.split('\n'):
                 index = line.find('WORD="')
                 if index != -1:
                     line = line[index+6:line.find('"', index+6)]
                     strTemp += str(line)

                if strTemp == 'バイバイ':
                    if killword != 'バイバイ':
                        print("Result: " + strTemp)
                        # os.system("aplay '/home/pi/Music/byebye.wav'")
                        print("<<<please speak1>>>")
                        killword = "バイバイ1111"

                elif strTemp == 'おはよう':
                    if killword != 'おはよう':
                        print("Result: " + strTemp)
                        # os.system("aplay '/home/pi/Music/ohayo.wav'")
                        print("<<<please speak2>>>")
                        killword = "おはよう2222"

                elif strTemp == 'こんにちは':
                    if killword != "こんにちは":
                        print("Result: " + strTemp)
                        # os.system("aplay '/home/pi/Music/konnichiwa.wav'")
                        print("<<<please speak3>>>")
                        killword = "こんにちは3333"

                elif strTemp == 'こんばんは':
                    if killword != "こんばんは":
                        print("Result: " + strTemp)
                        # os.system("aplay '/home/pi/Music/konbanwa.wav'")
                        print("<<<please speak4>>>")
                        killword = "こんばんは4444"

                elif strTemp == 'こんばんは':
                    if killword != "こんばんは":
                        print("Result: " + strTemp)
                        # os.system("aplay '/home/pi/Music/konbanwa.wav'")
                        print("<<<please speak5>>>")
                        killword = "こんばんは5555"

                else:
                    print("Result:" + strTemp)

                    # Talk_APIで追加
                    response = client.talk(strTemp)
                    print("<<<Talk_API>>> " +
                          ((response['results'])[0])['reply'])

                    i = randint(3)
                    if i == 0:
                        # os.system("aplay: '/home/pi/Music/aizuchi00.wav'")
                        # elif i == 1:
                        # os.system("aplay: '/home/pi/Music/aizuchi01.wav'")
                        # elif i == 2:
                        # os.system("aplay: '/home/pi/Music/aizuchi02.wav'")
                        print("<<<please speak6>>>")
                        data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
