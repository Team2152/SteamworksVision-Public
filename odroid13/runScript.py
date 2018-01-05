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
from collections import deque

def con(pic1, pic2, a):
      return np.concatenate((pic1, pic2),axis=a)

class image_manager:
	
  def quad(self, feeds):
    (feed1, feed2, feed3, feed4) = feeds
    return con(con(feed1, feed2, 1),con(feed3, feed4, 1),0)
  
  def __init__(self, status):
    self.image_pub = rospy.Publisher("/quad_feed",Image)
    #self.update_pub = rospy.Publisher("/updates",String)
    
    self.bridge = CvBridge()
    
    self.feeds = np.zeros((4,240,320,3), np.uint8)
    self.Qs = [deque(maxlen=2), deque(maxlen=2), deque(maxlen=2), deque(maxlen=2)]
    
    #self.update_sub = rospy.Subcriber("/updates",String,self.updateQuad)
    self.sub_11_0 = rospy.Subscriber("/uc0/image_raw",Image,self.callback110)
    self.sub_11_1 = rospy.Subscriber("/uc1/image_raw",Image,self.callback111)
    self.sub_12_0 = rospy.Subscriber("/uc0_12/image_raw",Image,self.callback120)
    self.sub_12_1 = rospy.Subscriber("/uc1_12/image_raw",Image,self.callback121)
    
    self.status = status
  
  def updateQuad(self, data):
    i = 0
    while i < 4:
        if (len(self.Qs[i]) > 0):
            self.feeds[i] = self.Qs[i].pop()
        i+=1
    bigPicture = self.quad(self.feeds)
    self.image_pub.publish(self.bridge.cv2_to_imgmsg(bigPicture, "bgr8"))
      
  def callback110(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.Qs[0].append(cv_image)
      #self.update_pub.publish("110")
      self.updateQuad("null")
    except CvBridgeError as e:
      print(e)
  
  def callback111(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.Qs[1].append(cv_image)
      #self.update_pub.publish("111")
    except CvBridgeError as e:
      print(e)

  def callback120(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.Qs[2].append(cv_image)
      #self.update_pub.publish("120")
    except CvBridgeError as e:
      print(e)

  def callback121(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.Qs[3].append(cv_image)
      #self.update_pub.publish("121")
    except CvBridgeError as e:
      print(e)
    

def run(status):
  im = image_manager(status)
  rospy.init_node('image_manager', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  #cv2.destroyAllWindows()
