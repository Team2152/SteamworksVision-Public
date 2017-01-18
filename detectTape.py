import cv2
# import cv2.cv as cv
import numpy as np
import math as m
from operator import itemgetter

def gearInfo():
    lowHue = 114
    highHue = 260
    lowSat = 40
    highSat = 125
    lowIntensity = 0
    highIntensity = 80
    lowBound = (lowHue, lowSat, lowIntensity)
    highBound = (highHue, highSat, highIntensity)
    setDist = 25.5  # inches
    setHeight = 150  # pixels
    return (lowBound, highBound), setDist, setHeight

def boilerInfo():
    lowHue = 114
    highHue = 238
    lowSat = 40
    highSat = 125
    lowIntensity = 0
    highIntensity = 80
    lowBound = (lowHue, lowSat, lowIntensity)
    highBound = (highHue, highSat, highIntensity)
    setDist = 30  # inches
    setHeight = 30  # Pixels
    return (lowBound, highBound), setDist, setHeight

def detectTape(tapeLocation, cameraNumber):

    if (tapeLocation == "G"):
        print gearInfo()
        bounds, setDist, setHeight = gearInfo()
    else:
        bounds, setDist, setHeight = boilerInfo()

    lowBound, highBound = bounds

    camera = cv2.VideoCapture(cameraNumber)

    while True:
        (grabbed, frame) = camera.read()

        mask = cv2.inRange(frame, lowBound, highBound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]
            count = len(cnts)
            cut = False
            i = 0
            if count > 2:
                count = 2
                if tapeLocation == "G":
                    cut = True

            for cnt in cnts[:count]:
                i = i + 1
                if cnt is not None and cv2.contourArea(cnt) > 100:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if i == 1:
                        cnt1 = cnt
                    if i == 2 and cut:
                        x2, y2, w2, h2 = cv2.boundingRect(cnts[2])
                        if x2 < x + 5 and x2 > x - 5:
                            cnt = np.concatenate((cnt,cnts[i]), axis=0)
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(frame, [box], 0, (255, 0 ,0), 2)
                    if i == 2:
                        pegBox = np.concatenate((cnt1,cnt), axis=0)
                        pegArea = np.int0(cv2.boxPoints(cv2.minAreaRect(pegBox)))
                        pegX = (pegArea[0][0]+pegArea[1][0]+pegArea[2][0]+pegArea[3][0])/4
                        pegY = (pegArea[0][1]+pegArea[1][1]+pegArea[2][1]+pegArea[3][1])/4
                        height1 = abs(pegArea[0][1] - pegArea[1][1])
                        height2 = abs(pegArea[1][1] - pegArea[2][1])
                        height3 = abs(pegArea[2][1] - pegArea[3][1])
                        height4 = abs(pegArea[3][1] - pegArea[0][1])
                        heights = [height1,height2,height3,height4]
                        heights = sorted(heights, reverse=True)
                        pixels = heights[0]
                        if (heights[0] != 0):
                            distance = 3780/pixels
                        else:
                            distance = 0
                        targetPeg = (pegX,pegY)
                        cv2.drawContours(frame, [pegArea], 0, (0, 0, 255), 4)
                        cv2.line(frame, targetPeg, targetPeg, (255, 0, 255), 20)
                        shooterXAngle = (((targetPeg[0]) * 52.4)/640) - 26.2
                        shooterYAngle = (((targetPeg[1]) * -43.4)/480) + 22.7
                        cv2.putText(mask, "X Angle: " + str(shooterXAngle), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                        cv2.putText(mask, "Y Angle: " + str(shooterYAngle), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                        cv2.putText(mask, "Pixel Count: " + str(pixels), (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                        cv2.putText(mask, "Distance: " + str(distance), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    #hull = cv2.convexHull(cnt)
                    #cv2.drawContours(frame, [hull], 0, (255, 255, 0), 4)

        frame = cv2.resize(frame, (320, 240))
        mask = cv2.resize(mask, (320, 240))
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    camera.release()

detectTape("G", 1)