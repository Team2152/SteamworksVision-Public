import cv2
# import cv2.cv as cv
import numpy as np
import math as m

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
highHue = 122  # 361
lowSat = 40  # 70
highSat = 100  # 255
lowIntensity = 0  # 0
highIntensity = 204  # 204

cv2.namedWindow("Trackbars", 0)


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
    # cv2.imshow("testing",frame)
    mask = cv2.inRange(frame, (lowHue, lowSat, lowIntensity), (highHue, highSat, highIntensity))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    lines = frame.copy()

    # cv2.imshow("lines",lines)
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=False)[:10]
        cnt = None
        for e in cnts:
            M = cv2.moments(e)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.line(frame, (cx, cy), (cx, cy), (255, 0, 255), 20)
            x, y, w, h = cv2.boundingRect(e)
            if cv2.contourArea(e) > 400:
                cnt = e
        if cnt is not None:
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)
            hull = cv2.convexHull(cnt)
            cv2.drawContours(frame, [hull], 0, (255, 255, 0), 4)

    cv2.drawContours(frame, cnts, -1, (0, 0, 255), 3)
    frame = cv2.resize(frame, (320, 240))
    mask = cv2.resize(mask, (320, 240))
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
camera.release()
