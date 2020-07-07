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
                            print("if分岐完了: 「こんにちは」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text0.wav'")

                        elif text[0].find('電気グモを買って') != -1:
                            # 発話2
                            print("if分岐完了: 「電気グモを買って」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text1.wav'")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text2.wav'")

                        elif text[0].find('そこをなんとか') != -1:
                            # 発話3
                            print("if分岐完了: 「そこをなんとか」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text3.wav'")

                        elif text[0].find('了解') != -1:
                            # 発話4
                            print("if分岐完了: 「了解」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text4.wav'")

                        elif text[0].find('どうも') != -1:
                            # 発話5
                            print("if分岐完了: 「どうも」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text6.wav'")

                        elif text[0].find('退勤') != -1:
                            # 発話6
                            print("if分岐完了: 「退勤」を認識しました。")
                            print("<<<認識スタート>>>")
                            # 自分で作成した学習モデルを読み込む
                            recognizer = cv2.face.LBPHFaceRecognizer_create()
                            recognizer.read(
                                '/home/pi/face/trainer/trainer.yml')

                            cascadePath = "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascadePath)
                            font = cv2.FONT_HERSHEY_SIMPLEX

                            id = 0
                            # ユーザーIDを名前に置き換えるためのリストを作る
                            # 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
                            names = ['None', 'pi', 'raspberry',
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
                                    cv2.putText(
                                        img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
                                    # 信頼度(%)を表示
                                    cv2.putText(img, str(confidence), (x+5, y+h-5),
                                                font, 1, (255, 255, 0), 1)

                                cv2.imshow('camera', img)
                                k = cv2.waitKey(10) & 0xff
                                if k == 27:
                                    break

                            print("プログラムを終了します。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text7.wav'")

                        elif text[0].find('伝言') != -1:
                            # 発話7
                            print("if分岐完了: 「伝言」を認識しました。")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text8.wav'")

                        elif text[0].find('退社') != -1:
                            # 発話8
                            print("if分岐完了: 「退社」を認識しました。")
                            print("<<<認識スタート>>>")
                            # 自分で作成した学習モデルを読み込む
                            recognizer = cv2.face.LBPHFaceRecognizer_create()
                            recognizer.read('/home/pi/face/trainer/trainer.yml')

                            cascadePath = "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascadePath)
                            font = cv2.FONT_HERSHEY_SIMPLEX

                            id = 0
                            # ユーザーIDを名前に置き換えるためのリストを作る
                            # 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
                            names = ['None', 'pi', 'raspberry', 'test1', 'test1', 'test3']

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
                                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    # 顔認識の信頼度を取得 100～0 0の時が100%一致
                                    id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                                    if (confidence < 100):
                                        # 顔認識しているidから名前に変換
                                        id = names[id]
                                        confidence = "  {0}%".format(round(100 - confidence))
                                    else:
                                        id = "unknown"
                                        confidence = "  {0}%".format(round(100 - confidence))

                                    # 名前を表示
                                    cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
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
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text9.wav'")
                            os.system("aplay '/home/pi/Desktop/Lab9_team_dev/julius/dictation-kit-4.5/text10.wav'")

                        elif text[0].find('認識') != -1:
                            print("if分岐完了: 「認識」を認識しました。")
                            print("<<<認識スタート>>>")
                            # 自分で作成した学習モデルを読み込む
                            recognizer = cv2.face.LBPHFaceRecognizer_create()
                            recognizer.read('/home/pi/face/trainer/trainer.yml')

                            cascadePath = "/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascadePath)
                            font = cv2.FONT_HERSHEY_SIMPLEX

                            id = 0
                            # ユーザーIDを名前に置き換えるためのリストを作る
                            # 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
                            names = ['None', 'pi', 'raspberry', 'test1', 'test1', 'test3']

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
                                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    # 顔認識の信頼度を取得 100～0 0の時が100%一致
                                    id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                                    if (confidence < 100):
                                        # 顔認識しているidから名前に変換
                                        id = names[id]
                                        confidence = "  {0}%".format(round(100 - confidence))
                                    else:
                                        id = "unknown"
                                        confidence = "  {0}%".format(round(100 - confidence))

                                    # 名前を表示
                                    cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
                                    # 信頼度(%)を表示
                                    cv2.putText(img, str(confidence), (x+5, y+h-5),
                                                font, 1, (255, 255, 0), 1)

                                cv2.imshow('camera', img)
                                k = cv2.waitKey(10) & 0xff
                                if k == 27:
                                    break

                            print("プログラムを終了します。")

                        elif text[0].find('学習') != -1:
                            print("if分岐完了: 「学習」を認識しました。")
                            print("<<<学習スタート>>>")
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

                            print("{0}種類の顔を学習しました。プログラムを終了します。".format(len(np.unique(ids))))

                        elif text[0].find('撮影') != -1:
                        print("if分岐完了: 「撮影」を認識しました。")
                        print("<<<撮影スタート>>>")
                        cam = cv2.VideoCapture(0)
                        cam.set(3, 640)
                        cam.set(4, 480)
                        face_detector = cv2.CascadeClassifier(
                            '/home/pi/face/model/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')

                        # ユーザーIDの入力
                        face_id = input('ユーザーID(1,2,3...)を入力して、Enterキーを押してください。')
                        print("画像データを収集しています。カメラを見てしばらくお待ちください。")

                        # 画像データ(写真)を何枚撮ったか数えるカウンター変数
                        count = 0
                        while(True):
                            ret, img = cam.read()
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces = face_detector.detectMultiScale(gray, 1.3, 5)
                            for (x, y, w, h) in faces:
                                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                                count += 1
                                # dataset/フォルダにUser*と名前を付けて写真を保存
                                cv2.imwrite("/home/pi/face/dataset/User." + str(face_id) +
                                            '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])
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
                        # VUIの終了
                        # 最後データの初期化
                        data = ""

                        # NULLの時の処理
                else:
                    # print("<<<please speak>>>")
                    data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
