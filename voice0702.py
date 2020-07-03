# -*- coding: utf-8 -*-
import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time

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
            strTemp = ""
            for line in data.split('\n'):
                index = line.find('WORD="')
                if index != -1:
                    line = line[index+6:line.find('"', index+6)]
                    strTemp += str(line)

                else:
                    print("Result:" + strTemp)

                    i = randint(3)
                    if i == 0:
                        print("<<<please speak6>>>")
                        data = ""
        else:
            data += str(sock.recv(1024).decode('utf-8'))
