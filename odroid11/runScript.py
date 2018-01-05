#!/usr/bin/env python
from __future__ import print_function
import tapeDetector
import cv2

#def run(queue, status):
#	camera = cv2.VideoCapture(0) 
#	myTapeDetector = tapeDetector.tapeDetector("peg", queue)
#	while not status.isStopped():
#		grabbed, frame = camera.read()
#		key = cv2.waitKey(1) & 0xFF
#		if key == ord("q"):
#			break
#		result, mask = myTapeDetector.detectTape(frame)
		#cv2.imshow("window1", result)
		#cv2.imshow("window2", mask)
#	camera.release
#	cv2.destroyAllWindows


import roslib
roslib.load_manifest('swv')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self, queue, status, camera):
    self.image_pub = rospy.Publisher("/uc" + str(camera) + "/image_cv",Image)
    self.image_pub2 = rospy.Publisher("/uc" + str(camera) + "/image_mask",Image)
    self.bridge = CvBridge()
    self.camera = camera
    self.image_sub = rospy.Subscriber("/uc" + str(camera) + "/image_raw",Image,self.callback)
    self.queue = queue
    self.status = status

    if (camera == 1):
        self.myTapeDetector = tapeDetector.tapeDetector("peg", self.queue)

    
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      if (self.camera == 1):
		cv_image, mask = self.myTapeDetector.detectTape(cv_image)
      
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
   # cv2.imshow("Image window", cv_image)
   # cv2.waitKey(3)

    try:
      if self.camera == 1:
        self.image_pub2.publish(self.bridge.cv2_to_imgmsg(mask,"mono8"))
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
      #self.image_pub.publish(data)
      #print("callback1")
      #print("callback1")
    except CvBridgeError as e:
      print(e)

def run(queue, status):
    ic = image_converter(queue, status, 1)
    ic2 = image_converter(queue, status, 0)
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down...")

  #cv2.destroyAllWindows()
