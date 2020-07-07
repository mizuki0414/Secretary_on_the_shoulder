# -*- coding: utf-8 -*-
import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time
import numpy as np
import cv2
import time

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
                    text = line.split('\n')
                    index_cm = text[0].find('1.000')
                    print(index_cm)
                    if index_cm != -1:
                        # このif文を参考に以後の処理を修正ください
                        if text[0].find('こんにちは') != -1:
                            # 発話1
                            print("if分岐完了: こんにちはを認識しました。")
                            os.system(
                                "aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/welcome.wav'")

                        elif recog_text == '写真':
                            # 発話2
                            print("if分岐完了: 写真を撮影します。")
                            os.system(
                                "aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/take.wav'")

                        elif recog_text == '開始':
                            # カメラで動画を撮影する カメラ1台の場合は引数に0 or -1を設定する
                            faceCascade = cv2.CascadeClassifier(
                                '/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
                            cap = cv2.VideoCapture(0)
                            cap.set(3, 640)  # 横幅を設定
                            cap.set(4, 480)  # 縦幅を設定
                            ut1 = time.time()  # 現在時刻
                            while True:
                                # ループ内の経過時間を計測
                                ut2 = time.time()  # 現在時刻
                                t_pass = ut2 - ut1
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
                                for (x, y, w, h) in faces:
                                    cv2.rectangle(
                                        img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                                    roi_gray = gray[y:y+h, x:x+w]
                                    roi_color = img[y:y+h, x:x+w]

                                # imshow関数で結果を表示する
                                cv2.imshow('video', img)

                                # ESCが押されたら終了する
                                k = cv2.waitKey(30) & 0xff
                                if t_pass >= 10:
                                    # if k == 27:
                                    break

                            cap.release()
                            cv2.destroyAllWindows()

                        elif recog_text == '撮影':
                            cam = cv2.VideoCapture(0)
                            cam.set(3, 640)
                            cam.set(4, 480)
                            face_detector = cv2.CascadeClassifier(
                                '/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')

                            # ユーザーIDの入力
                            face_id = input(
                                'ユーザーID(1,2,3...)を入力して、Enterキーを押してください。')
                            print("画像データを収集しています。カメラを見てしばらくお待ちください。")

                            # 画像データ(写真)を何枚撮ったか数えるカウンター変数
                            count = 0
                            while(True):
                                ret, img = cam.read()
                                print('撮影中')
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                faces = face_detector.detectMultiScale(
                                    gray, 1.3, 5)
                                for (x, y, w, h) in faces:
                                    cv2.rectangle(
                                        img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                                    count += 1
                                    # dataset/フォルダにUser*と名前を付けて写真を保存
                                    cv2.imwrite("/home/pi/face/dataset/User." + str(
                                        face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])
                                    cv2.imshow('image', img)

                                # ESCキーを押すか、30枚写真を撮ったら終了
                                k = cv2.waitKey(100) & 0xff
                                if k == 27:
                                    print("画像データの収集を中断しました。")
                                    break
                                elif count >= 30:
                                    print("画像データの収集が完了しました。")
                                    break

                            cam.release()
                            cv2.destroyAllWindows()

                        elif recog_text == '学習':
                            # 画像データのパスを指定
                            path = '/home/pi/face/dataset'
                            # 顔認識のためにOpenCVモジュールのLBPH（LOCAL BINARY PATTERNS HISTOGRAMS)のインスタンスを生成
                            recognizer = cv2.face.LBPHFaceRecognizer_create()
                            detector = cv2.CascadeClassifier(
                                "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml")

                            # 画像データとラベル(id)を取得する関数
                            def getImagesAndLabels(path):
                                imagePaths = [os.path.join(
                                    path, f) for f in os.listdir(path)]
                                faceSamples = []  # 画像データを格納するリスト
                                ids = []  # idを格納するリスト

                                # datasetフォルダ内にある全フォルダをループで回す
                                # 画像をグレースケール化してfaceSamplesリストに追加、idはidsリストに追加
                                for imagePath in imagePaths:
                                    PIL_img = Image.open(imagePath).convert(
                                        'L')  # グレースケールに変換
                                    img_numpy = np.array(PIL_img, 'uint8')
                                    id = int(os.path.split(imagePath)
                                             [-1].split(".")[1])
                                    faces = detector.detectMultiScale(
                                        img_numpy)
                                    for (x, y, w, h) in faces:
                                        faceSamples.append(
                                            img_numpy[y:y+h, x:x+w])
                                        ids.append(id)
                                return faceSamples, ids
                            print("学習中です。しばらくお待ちください。")

                            # 上記関数を使用して、グレースケール化した画像とユーザーIDを取得
                            faces, ids = getImagesAndLabels(path)

                            # 学習する
                            recognizer.train(faces, np.array(ids))

                            # 学習済みモデルをtrainer/trainer.ymlファイルに出力する
                            recognizer.write(
                                '/home/pi/face/trainer/trainer.yml')

                            print("{0}種類の顔を学習しました。プログラムを終了します。".format(
                                len(np.unique(ids))))

                        # VUIの終了
                        # 最後データの初期化
                        data = ""

                        # NULLの時の処理
                else:
                    # print("<<<please speak>>>")
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
