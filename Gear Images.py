import cv2
import numpy as np
import math as m
from time import sleep

camera = cv2.VideoCapture(0)
fileNum = 1
mode = 'gearExample'
while True:
    (grabbed, frame) = camera.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("p"):
        cv2.imwrite(mode + str(fileNum)+ '.png',frame)
        fileNum+=1
camera.release()
