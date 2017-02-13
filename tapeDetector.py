import cv2
import cv2 as cv
import numpy as np
import math as m
from operator import itemgetter
from DataPacket import *

def pegInfo():
    lowHue = 46  # 126
    highHue = 260  # 361
    lowSat = 0  # 70
    highSat = 71  # 255
    lowIntensity = 0  # 0
    highIntensity = 28  # 204
    lowBound = (lowHue, lowSat, lowIntensity)
    highBound = (highHue, highSat, highIntensity)
    thirdParam = "Parallax"
    return (lowBound, highBound), thirdParam

def boilerInfo():
    lowHue = 35
    highHue = 54
    lowSat = 27
    highSat = 32
    lowIntensity = 13
    highIntensity = 70
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
		frame = imageIn
		mask = cv2.inRange(frame, self.lowBound, self.highBound)
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
				cut = self.tape == "peg"
			for cnt in cnts[:count]:
				i += 1
				if cnt is not None and cv2.contourArea(cnt) > 100:
					x, y, w, h = cv2.boundingRect(cnt)
					if i == 1:
						cnt1 = cnt
					if i == 2 and cut:
						x2, y2, w2, h2 = cv2.boundingRect(cnts[2])
						if x2 < x + 5 and x2 > x - 5:
							cnt = np.concatenate((cnt,cnts[i]), axis=0)
					rect = cv2.minAreaRect(cnt)
					box = cv.boxPoints(rect)
					box = np.int0(box)
					cv2.drawContours(frame, [box], 0, (255, 0 ,0), 2)
					if i == 2:
						pegBoth = np.concatenate((cnt1,cnt), axis=0)
						pegArea = np.int0(cv.boxPoints(cv2.minAreaRect(pegBoth)))
						pegYs = sorted([pegArea[0][1], pegArea[1][1], pegArea[2][1], pegArea[3][1]])
						pegX = (pegArea[0][0]+pegArea[1][0]+pegArea[2][0]+pegArea[3][0])/4
						pegY = (pegArea[0][1]+pegArea[1][1]+pegArea[2][1]+pegArea[3][1])/4
						
						height1 = abs(pegArea[0][1] - pegArea[1][1])
						height2 = abs(pegArea[1][1] - pegArea[2][1])
						height3 = abs(pegArea[2][1] - pegArea[3][1])
						height4 = abs(pegArea[3][1] - pegArea[0][1])
						heights = sorted([height1,height2,height3,height4], reverse=True)
						h = (heights[0] + heights[1])/2
						width1 = abs(pegArea[0][0] - pegArea[1][0])
						width2 = abs(pegArea[1][0] - pegArea[2][0])
						width3 = abs(pegArea[2][0] - pegArea[3][0])
						width4 = abs(pegArea[3][0] - pegArea[0][0])
						widths = sorted([width1,width2,width3,width4], reverse=True)
						w = (widths[0] + widths[1])/2
						
						#pixels = heights[0] # +heights[1] ) /2 # Add this later (will need to retune)
						#pixelsNew = (heights[0]+heights[1])/2
						
						targetPeg = (pegX,pegY)
						
						adj = 319.5 * m.tan(m.radians(90-37.5))
						xAngle = m.degrees(m.atan((targetPeg[0]-319.5)/adj))
						
						adj2 = (239.5 * m.tan(m.radians(90-30)))
						yAngle = m.degrees(m.atan((targetPeg[1]-239.5)/adj2))
						
						
						if (h != 0):
							
							result = (5.5 * w) / (10.5 * h * 15/16)
							if result > 1:
								result = 1
							elif result < -1:
								result = -1
							parallax = m.degrees(m.acos(result))
							
						else:
							parallax = 0
						
						#parallax = 0 
						avgY = (pegYs[2]+pegYs[3])/2
						cv2.line(frame, (0,avgY), (640,avgY), (255,200,49))
						bottomYAngle = m.atan((avgY-239.5)/adj2)
						distance = 8.25/m.tan(bottomYAngle)
						
						cv2.drawContours(frame, [pegArea], 0, (0, 0, 255), 4)
						cv2.line(frame, targetPeg, targetPeg, (255, 0, 255), 20)

						cv2.putText(mask, "X Angle: " + str(xAngle), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Y Angle: " + str(yAngle), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Distance: " + str(distance), (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
						cv2.putText(mask, "Parallax: " + str(parallax), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
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
