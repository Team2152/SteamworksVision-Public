import cv2
# import cv2.cv as cv
import numpy as np
import math as m
from time import sleep
lowVal = (0, 90, 112)
highVal = (20, 201, 255)
camera = cv2.VideoCapture(0)
global lowHue
global highHue
global lowSat
global highSat
global lowIntensity
global highIntensity

lowHue = 0  # 126
highHue = 255  # 361
lowSat = 0  # 70
highSat = 88  # 255
lowIntensity = 70  # 0
highIntensity = 255  # 204

cv2.namedWindow("Trackbars", 0)
i = 0
def callback1(value):
    global lowHue
    lowHue = value

def callback2(value):
    global highHue
    highHue = value


def callback3(value):
    global lowSat
    lowSat = value

def callback4(value):
    global highSat
    highSat = value


def callback5(value):
    global lowIntensity
    lowIntensity = value


def callback6(value):
    global highIntensity
    highIntensity = value

cv2.createTrackbar("lowHue", "Trackbars", lowHue, 360, callback1)
cv2.createTrackbar("highHue", "Trackbars", highHue, 360, callback2)
cv2.createTrackbar("lowSat", "Trackbars", lowSat, 256, callback3)
cv2.createTrackbar("highSat", "Trackbars", highSat, 256, callback4)
cv2.createTrackbar("lowIntensity", "Trackbars", lowIntensity, 256, callback5)
cv2.createTrackbar("highIntensity", "Trackbars", highIntensity, 256, callback6)

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.resize(frame, (320, 240))
    frame2 = frame.copy()
    
    mask1 = cv2.inRange(frame2, (0, 0, 70), (255, 88, 255))
    mask1 = cv2.erode(mask1, None, iterations=1)
    mask1 = cv2.dilate(mask1, None, iterations=1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    frame2 = cv2.absdiff(gray2, frame)

    cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(frame, (110, 0, 0), (255, 255, 255)) # HighSat = 210 also works
    mask2 = cv2.erode(mask2, None, iterations=1)
    mask2 = cv2.dilate(mask2, None, iterations=1)

    mask3= cv2.inRange(frame2, (25, 0, 0), (256, 256, 256))
    mask3= cv2.erode(mask3, None, iterations=1)
    mask3= cv2.dilate(mask3, None, iterations=1)

    maskFinal = mask3 - mask2 - mask1
    maskFinal = cv2.inRange(maskFinal, 2, 300)

    cnts = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    lines = frame.copy()

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=False)[:10]
        cnt = None
        for e in cnts:
            M = cv2.moments(e)
            if cv2.contourArea(e) > 200:
                cnt = e
        for cnt in cnts:
            if cnt is not None and cv2.contourArea(cnt) > 300:
                M = cv2.moments(e)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    angleToGear = (((cx) * 52.4)/320) - 26.2
                else:
                    cx,cy = (None,None)
                cv2.line(frame, (cx, cy), (cx, cy), (0, 255, 0), 5)
                hull = cv2.convexHull(cnt)
                #cv2.drawContours(frame, [hull], 0, (255, 255, 0), -1)
                cv2.drawContours(frame, [cnt], 0, (255, 0, 255), 2)

    #cv2.drawContours(frame, cnts, -1, (0, 0, 255), 3)
    #frame = cv2.resize(frame, (320, 240))
    #mask3= cv2.resize(mask, (320, 240))

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", maskFinal)
    key = cv2.waitKey(1) & 0xFF
    sleep(0.1)
    if key == ord("q"):
        break
camera.release()

