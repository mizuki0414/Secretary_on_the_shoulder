# -*- coding: utf-8 -*-
import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time
import pya3rt

apikey = "DZZ0TIpd7cKXP0IgtSLNZQrVf7BnY8bv"  # Talk_APIキー
client = pya3rt.TalkClient(apikey)

host = "localhost"
port = 10500

p = subprocess.Popen(["./julius-start.sh"], stdout=subprocess.PIPE, shell=True)
pid = str(p.stdout.read().decode('utf-8'))  # juliusのプロセスIDを取得
time.sleep(5)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

data = ""  # dataの初期化
killword = ""  # 前回認識した言葉を記憶するための変数

while True:

    while (1):
        if '</RECOGOUT>\n.' in data:  # 出力結果から認識した単語を取り出す

            recog_text = ""

            for line in data.split('\n'):
                index = line.find('WORD="')
                if index != -1:
                    line = line[index+6:line.find('"', index+6)]
                    recog_text += str(line)
                    print("<<<Speakword>>>")
                    print(recog_text)
                    if recog_text == 'こんにちは':
                        print("if分岐完了: こんにちはを認識しました。")
                        os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/welcome.wav'")
                    elif recog_text == '写真':
                        print("if分岐完了: 写真を撮影します。")
                        os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/take.wav'")
                    data = ""

                    # NULLの時の処理
                else:
                    # print("<<<please speak>>>")
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))






