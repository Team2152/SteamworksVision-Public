import cv2
import numpy as np
import math as m
from time import sleep

global MouseX
global MouseY
MouseX = -1
MouseY = -1
Point1, Point2 = (0,0)
pictureCount = 3
count = 1
click1 = False
click2 = False
p1Set = False
p2Set = False
lastMousePoint = (-1,-1)
pictureInfo = []

def noteGear(event, x, y, flags, param):
    # grab references to the global variables
    global MouseX
    global MouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        MouseX = x
        MouseY = y

picture = cv2.imread("gearExample" + str(count) + ".png")
cv2.imshow("Window", picture)
cv2.setMouseCallback("Window", noteGear)

while count <= pictureCount:
    pictureName = "gearExample" + str(count) + ".png"
    picture = cv2.imread(pictureName)
    cv2.imshow("Window", picture)
    while p1Set == False or p2Set == False:
        cv2.imshow("Window", picture)
        cv2.waitKey(0)
        sleep(0.1)
        if p1Set == False and lastMousePoint != (MouseX,MouseY):
            print "Point 1 set"
            Point1 = (MouseX,MouseY)
            lastMousePoint = Point1
            p1Set = True
        elif p2Set == False and lastMousePoint != (MouseX,MouseY):
            print "Point 2 set"
            Point2 = (MouseX,MouseY)
            lastMousePoint = Point2
            break
    pictureInfo.append(pictureName + " " + str(Point1[0]) + " " + str(Point1[1]) + " " + str(Point2[0]) + " " + str(Point2[1]))
    print pictureName + " " + str(Point1[0]) + " " + str(Point1[1]) + " " + str(Point2[0]) + " " + str(Point2[1])
    p1Set = False
    p2Set = False
    count += 1

print "List:"
for x in pictureInfo:
    print x

