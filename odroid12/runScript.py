#!/usr/bin/env python
from __future__ import print_function
import tapeDetector
import cv2

import roslib
roslib.load_manifest('swv')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class image_converter:

  def __init__(self, queue, status, camera):
    self.image_pub = rospy.Publisher("/uc" + str(camera) + "_12/image_cv",Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/uc" + str(camera) + "_12/image_raw",Image,self.callback)
    self.queue = queue
    self.status = status
    self.camera = camera
    if (camera == 0):
        self.myTapeDetector = tapeDetector.tapeDetector("boiler", self.queue)
    
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape

    try:
      
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))

    except CvBridgeError as e:
      print(e)

def run(queue, status):
  ic = image_converter(queue, status, 1)
  ic2 = image_converter(queue, status, 0)
  rospy.init_node('image_converter', anonymous=True)
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  #cv2.destroyAllWindows()
