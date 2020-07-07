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
import time

# TalkAPI用のキー
apikey = "DZZ0TIpd7cKXP0IgtSLNZQrVf7BnY8bv"  # Talk_APIキー
client = pya3rt.TalkClient(apikey)

host = "localhost"
port = 10500

p = subprocess.Popen(["./julius-start.sh"], stdout=subprocess.PIPE, shell=True)
pid = str(p.stdout.read().decode('utf-8'))  # juliusのプロセスIDを取得
time.sleep(3)
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
                        print("if分岐完了: 「こんにちは」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/text0.wav'")

                    elif recog_text == '電気グモを買って':
                        # 発話2
                        print("if分岐完了: 「電気グモを買って」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/text1.wav'")
                        time.sleep(3)
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/text2.wav'")

                    elif recog_text == 'そこをなんとか':
                        # 発話3
                        print("if分岐完了: 「そこをなんとか」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/text3.wav'")

                    elif recog_text == '了解':
                        # 発話4
                        print("if分岐完了: 「了解」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/text4.wav'")

                    elif recog_text == '退勤':
                        # 発話5
                        # 自分で作成した学習モデルを読み込む
                        print("if分岐完了: 退勤処理。")
                        recognizer = cv2.face.LBPHFaceRecognizer_create()
                        recognizer.read('/home/pi/face/trainer/trainer.yml')

                        cascadePath = "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
                        faceCascade = cv2.CascadeClassifier(cascadePath)
                        font = cv2.FONT_HERSHEY_SIMPLEX

                        id = 1
                        # ユーザーIDを名前に置き換えるためのリストを作る
                        # 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
                        names = ['None', '柳原(営業一課)', 'ゆん(営業一課)',
                                 'test1', 'test1', 'test3']

                        cam = cv2.VideoCapture(0)
                        cam.set(3, 640)
                        cam.set(4, 480)

                        # 顔として認識する最小サイズを定義する
                        minW = 0.1 * cam.get(3)
                        minH = 0.1 * cam.get(4)

                        while True:
                            ret, img = cam.read()
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                            faces = faceCascade.detectMultiScale(
                                gray,
                                scaleFactor=1.2,
                                minNeighbors=5,
                                minSize=(int(minW), int(minH)),
                            )
                            for(x, y, w, h) in faces:
                                cv2.rectangle(
                                    img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                # 顔認識の信頼度を取得 100～0 0の時が100%一致
                                id, confidence = recognizer.predict(
                                    gray[y:y+h, x:x+w])
                                if (confidence < 100):
                                    # 顔認識しているidから名前に変換
                                    id = names[id]
                                    confidence = "  {0}%".format(
                                        round(100 - confidence))
                                else:
                                    id = "unknown"
                                    confidence = "  {0}%".format(
                                        round(100 - confidence))

                                # 名前を表示
                                cv2.putText(img, str(id), (x+5, y-5),
                                            font, 1, (255, 255, 255), 2)
                                # 信頼度(%)を表示
                                cv2.putText(img, str(confidence), (x+5, y+h-5),
                                            font, 1, (255, 255, 0), 1)

                            cv2.imshow('camera', img)
                            k = cv2.waitKey(10) & 0xff
                            if k == 27:
                                break

                        print("プログラムを終了します。")
                        cam.release()
                        cv2.destroyAllWindows()

                        print("if分岐完了: 「退勤」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/XXX.wav'")

                    elif recog_text == '退社':
                        # 発話2
                        print("if分岐完了: 退社処理。")
                        # 自分で作成した学習モデルを読み込む
                        recognizer = cv2.face.LBPHFaceRecognizer_create()
                        recognizer.read('/home/pi/face/trainer/trainer.yml')

                        cascadePath = "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
                        faceCascade = cv2.CascadeClassifier(cascadePath)
                        font = cv2.FONT_HERSHEY_SIMPLEX

                        id = 2
                        # ユーザーIDを名前に置き換えるためのリストを作る
                        # 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
                        names = ['None', '柳原(営業一課)', 'ゆん(営業一課)',
                                 'test1', 'test1', 'test3']

                        cam = cv2.VideoCapture(0)
                        cam.set(3, 640)
                        cam.set(4, 480)

                        # 顔として認識する最小サイズを定義する
                        minW = 0.1 * cam.get(3)
                        minH = 0.1 * cam.get(4)

                        while True:
                            ret, img = cam.read()
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                            faces = faceCascade.detectMultiScale(
                                gray,
                                scaleFactor=1.2,
                                minNeighbors=5,
                                minSize=(int(minW), int(minH)),
                            )
                            for(x, y, w, h) in faces:
                                cv2.rectangle(
                                    img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                # 顔認識の信頼度を取得 100～0 0の時が100%一致
                                id, confidence = recognizer.predict(
                                    gray[y:y+h, x:x+w])
                                if (confidence < 100):
                                    # 顔認識しているidから名前に変換
                                    id = names[id]
                                    confidence = "  {0}%".format(
                                        round(100 - confidence))
                                else:
                                    id = "unknown"
                                    confidence = "  {0}%".format(
                                        round(100 - confidence))

                                # 名前を表示
                                cv2.putText(img, str(id), (x+5, y-5),
                                            font, 1, (255, 255, 255), 2)
                                # 信頼度(%)を表示
                                cv2.putText(img, str(confidence), (x+5, y+h-5),
                                            font, 1, (255, 255, 0), 1)

                            cv2.imshow('camera', img)
                            k = cv2.waitKey(10) & 0xff
                            if k == 27:
                                break

                        print("プログラムを終了します。")
                        cam.release()
                        cv2.destroyAllWindows()

                        print("if分岐完了: 「退勤」を認識しました。")
                        os.system(
                            "aplay '/home/pi/Desktop/Lab9_team_dev/XXX.wav'")

                    # VUIの終了
                    # 最後データの初期化
                    data = ""

                    # NULLの時の処理
                else:
                    # print("<<<please speak>>>")
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
