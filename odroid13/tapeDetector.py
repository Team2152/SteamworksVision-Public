#!/usr/bin/env python
import cv2
import cv2 as cv
import numpy as np
import math as m
from operator import itemgetter
from DataPacket import *

def pegInfo():
    lowHue =        34   #35
    highHue =       247 #54
    lowSat =        31 #27
    highSat =       256 #32
    lowIntensity =  72 #13
    highIntensity = 256 #70
    lowBound = (lowHue, lowSat, lowIntensity)
    highBound = (highHue, highSat, highIntensity)
    thirdParam = "Parallax"
    return (lowBound, highBound), thirdParam

def boilerInfo():
    lowHue =        80   #260
    highHue =       260 #0
    lowSat =        160 #27
    highSat =       246 #32
    lowIntensity =  0 #13
    highIntensity = 63 #70
    lowBound = (lowHue, lowSat, lowIntensity)
    highBound = (highHue, highSat, highIntensity)
    thirdParam = "YAngle"
    return (lowBound, highBound), thirdParam

class tapeDetector():
	def __init__(self, tapeLocation, queue):
		self.Q = queue
		self.tape = tapeLocation
		self.packet = Packet()
		
		if tapeLocation == "peg":
			if True:
				self.packet.setItem(self.packet.Item.PEG)
			(self.lowBound, self.highBound), self.thirdParam = pegInfo()
		elif tapeLocation == "boiler":
			if True:
				self.packet.setItem(self.packet.Item.BOILER)
			(self.lowBound, self.highBound), self.thirdParam = boilerInfo()
		self.packet.params = [Param("xAngle", 0), Param("distance", 0), Param(self.thirdParam, 0)]

	def detectTape(self, imageIn):
		frame = cv2.cvtColor(imageIn, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(frame, self.lowBound, self.highBound)
		frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if(self.tape == "peg"):
			cv2.circle(frame, (20,20), 10, (255,20,100), 5)
		if len(cnts) > 0:
			cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]
			count = len(cnts)
			cut = False
			boxes = [None,None]
			i = 0
			if count > 2:
				count = 2
				cut = self.tape == "peg"
			for cnt in cnts[:count]:
				i += 1
				if cnt is not None and cv2.contourArea(cnt) > 50:
					x, y, w, h = cv2.boundingRect(cnt)
					if i == 1:
						x1, y1, w1, h1 = cv2.boundingRect(cnt)
						cnt1 = cnt
					if i == 2 and cut:
						x2, y2, w2, h2 = cv2.boundingRect(cnts[2])
						if x2 < x + 5 and x2 > x - 5:
							cnt = np.concatenate((cnt,cnts[i]), axis=0)
					rect = cv2.minAreaRect(cnt)
					box = cv.boxPoints(rect)
					box = np.int0(box)
					boxes[i-1] = box
					cv2.drawContours(frame, [box], 0, (255, 0 ,0), 2)
					if i == 2:
						pegBoth = np.concatenate((cnt1,cnt), axis=0)
						pegArea = np.int0(cv.boxPoints(cv2.minAreaRect(pegBoth)))
						pegYs = sorted([pegArea[0][1], pegArea[1][1], pegArea[2][1], pegArea[3][1]])
						pegX = float(pegArea[0][0]+pegArea[1][0]+pegArea[2][0]+pegArea[3][0])/4.0
						pegY = float(pegArea[0][1]+pegArea[1][1]+pegArea[2][1]+pegArea[3][1])/4.0
						heights = []
						for square in boxes:
							j = 0
							while j < 3:
								heights.append(abs(square[j][1]-square[j+1][1]))
								j+=1
							heights.append(abs(square[3][1]-square[0][1]))
						heights = sorted(heights, reverse=True)
						h = float(heights[0]+heights[1]+heights[2]+heights[3])/4.0
						
						width1 = abs(pegArea[0][0] - pegArea[1][0])
						width2 = abs(pegArea[1][0] - pegArea[2][0])
						width3 = abs(pegArea[2][0] - pegArea[3][0])
						width4 = abs(pegArea[3][0] - pegArea[0][0])
						widths = sorted([width1,width2,width3,width4], reverse=True)
						w = (widths[0] + widths[1])/2
						
						#pixels = heights[0] # +heights[1] ) /2 # Add this later (will need to retune)
						#pixelsNew = (heights[0]+heights[1])/2
						
						targetPeg = (int(pegX),int(pegY))
						cv2.line(frame, (int(pegX), int(pegY-(h/2.0))), (int(pegX), int(pegY+(h/2.0))), (99, 39, 200)) 
						res = (320.0, 240.0)
						adj = (res[0]/2-0.5) * m.tan(m.radians(90-37.5))
						xAngle = m.degrees(m.atan((pegX-(res[0]/2-0.5))/adj))
						
						adj2 = ((res[1]/2-0.5) * m.tan(m.radians(90-30)))
						yAngle = m.degrees(m.atan((pegY-(res[1]/2-0.5))/adj2))
						"""
						if (h != 0):
							result = (5.5 * w) / (10.5 * h * 15/16)
							if result > 1:
								result = 1
							elif result < -1:
								result = -1
							parallax = m.degrees(m.acos(result))
							
						else:
							parallax = 0
						"""
						
						#avgY = (pegYs[2]+pegYs[3])/2
						#cv2.line(frame, (0,avgY), (320,avgY), (255,200,49))
						#bottomYAngle = m.atan((avgY-119.5)/adj2)
						
						if(pegYs[3]>230 or pegYs[0] > 230 or pegYs[1] > 230 or pegYs[2] > 230):
							parallax = w
							distance = 2792.11/w
						else:
							parallax = h
							distance = 1350.68/h
							#distance = 19917.05/(14.0*h) #
							
							#distanceE = distance - err
						
						#err = ((distance-24)/35.0) - 1
						#distance = distance - (2**err)
						cv2.drawContours(frame, [pegArea], 0, (0, 0, 255), 4)
						cv2.line(frame, targetPeg, targetPeg, (255, 0, 255), 20)
						#cv2.rectangle(mask, (0,0), (320,240), 0, -1)
						cv2.putText(mask, "X Angle: " + str(xAngle), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Y Angle: " + str(yAngle), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Distance: " + str(distance), (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Parallax: " + str(parallax), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						#cv2.putText(mask, "Error: " + str(err), (10,190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						if (self.thirdParam == "yAngle"):
							thirdValue = yAngle
						else:
							thirdValue = parallax
						if True:
							self.packet.setParam("xAngle", xAngle)
							self.packet.setParam("distance", distance)
							self.packet.setParam(self.thirdParam, thirdValue)
							self.Q.put(self.packet)
		
		return frame, mask
