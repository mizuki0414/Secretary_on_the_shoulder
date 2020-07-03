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
import numpy as np
import cv2

# 学習済みモデルを読み込む
faceCascade = cv2.CascadeClassifier('/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
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
                        # 発話1
                        print("if分岐完了: こんにちはを認識しました。")
                        os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/welcome.wav'")
                    
                    elif recog_text == '写真':
                        # 発話2
                        print("if分岐完了: 写真を撮影します。")
                        os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/take.wav'")
                    
                    elif recog_text == 'ハロー':
                        # カメラ起動
                        # カメラで動画を撮影する カメラ1台の場合は引数に0 or -1を設定する
                        cap = cv2.VideoCapture(0)
                        cap.set(3,640) # 横幅を設定 
                        cap.set(4,480) # 縦幅を設定
                        while True: 
                            # フレーム毎にキャプチャする
                            ret, img = cap.read()

                            # 顔検出の負荷軽減のために、キャプチャした画像をモノクロにする
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            # 顔検出のパラメータの設定
                            faces = faceCascade.detectMultiScale(
                                gray,     
                                scaleFactor=1.2,
                                minNeighbors=5,     
                                minSize=(20, 20)
                            )
                            # 顔検出時に四角い枠を表示
                            for (x,y,w,h) in faces:
                                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                                roi_gray = gray[y:y+h, x:x+w]
                                roi_color = img[y:y+h, x:x+w]

                            # imshow関数で結果を表示する
                            cv2.imshow('video',img)
                            
                            # 終わりと言われたら終了する
                            # if recog_text == '終わり':
                            #   break
                            # ESCが押されたら終了する
                            k = cv2.waitKey(30) & 0xff
                            if k == 27: 
                                break
                        cap.release()
                        cv2.destroyAllWindows()
                    # 最後データの初期化
                    data = ""

                    # NULLの時の処理
                else:
                    # print("<<<please speak>>>")
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))






