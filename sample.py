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

    while (1):  # 無限ループ
        if '</RECOGOUT>\n.' in data:  # 出力結果から認識した単語を取り出す

            recog_text = ""

            for line in data.split('\n'):
                index = line.find('WORD="')
                if index != -1:
                    line = line[index+6:line.find('"', index+6)]
                    recog_text += str(line)

                    # if recog_text == 'おはよう':
                    #     print("Result: おはようございます")
                    #     print("<<<please speak>>>")
                    #     data = ""

                    print("Result: " + recog_text)

                    # Talk_APIで追加
                    response = client.talk(recog_text)
                    print("<<<Talk_API>>> " + ((response['results'])[0])['reply'])

                    data = ""

                # NULLの時の処理
                else:
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
