import cv2
from PIL import Image
import numpy as np
import sys
import glob
import os
from subprocess import call
from urllib.request import urlopen
from collections import Counter
import json
from pathlib import Path
import re

cf = 0
ResultStr = ['']

def LogicOpStrings():
    l = len(ResultStr)
    newArr = []
    for i in range(0, l):
        if not ResultStr[i]=="":
            newArr.append(ResultStr[i].replace("\n","").strip())

    newArrSet = set(newArr)

    url = ("https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json")
    print("Loading english dictionary from internet...")
    wordDic = get_jsonparsed_data(url)
    print("English word vocabulary has been successfully loaded!")
     
    validWordCountMap = []

    l = len(newArr)
    for i in range(0, l):
        count = 0
        wordChunks = newArr[i].split(' ')
        for j in range(0,len(wordChunks)):
            if wordChunks[j].lower() in wordDic:
                count = count + 1
            else:
                print(wordChunks[j]," is not a valid word!")
        validWordCountMap.append(count)


        print("-----Overall result:-----")
        print(newArr[validWordCountMap.index(most_Common(validWordCountMap))])
        print("-------------------------")

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

def tessfunc():   
    os.system("tesseract file.png data")
    clearTesseractExecNote()
    with open('data.txt', 'r') as mf:
        try:
            content = mf.read()
            if(not content.isspace()):
                ResultStr.append(content)
                print("\nResult:\n********************************************\n", re.sub('[^a-zA-Z\r\n]+', ' ', content),"\n********************************************")
        except UnicodeDecodeError:
            print("Unicode character found which cant be decoded")

def removechunk():
    for i in glob.glob('file*.png'):
        print("Unlinked %s" % i)
        os.unlink(i)

def clearTesseractExecNote():
    print ("\033[A                                                          \033[A")
    print ("\033[A                                                          \033[A")
 
print("Accessing device's camera...")
cap = cv2.VideoCapture(0)
print ("\033[A                                           \033[A")
print("Camera ready!")
print("Activated command mode!\nPress 's' to start text recognition")
count = 0
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Frame', gray)
    ret,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite('file.png', thresh)
    if cf == 1:
        tessfunc()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cf = 0 
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cf = 1
    if cv2.waitKey(1) & 0xFF == ord('e'):
        print("Terminating the program")
        break

cap.release()
exit()
