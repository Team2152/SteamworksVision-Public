import socket, sys, os, traceback, logging;
import multiprocessing;
import DataPacket;
import threading;
import time;

from subprocess import call 
from Utils import Status;
import Utils


def startCams(cameras):
	topic1 = ""
	topic2 = ""
	topic3 = ""
	topic4 = ""
	duration = 150
	if (cameras == "1"):
		topic1 = "/uc0/image_raw "
		topic2 = "/uc1/image_raw "
	"""
	if "1" in cameras:
		topic1 = "/uc0/image_raw "
	if "2" in cameras:
		topic2 = "/uc1/image_raw "
	if "3" in cameras:
		topic3 = "10.21.52.12:/uc0/image_raw "
	if "4" in cameras:
		topic4 = "10.21.52.12:/uc1/image_raw "
	"""
	if "T" in cameras:
		duration = 10
	
	parameters = "--duration=" + str(duration) + " -o DataTest"
	cmd1 = "cd /media/odroid/CORSAIR"
	cmd2 = "rosbag record " + topic1 + topic2 + topic3 + topic4 + parameters
	cmds = cmd1 + '''
	''' + cmd2
	return call(cmds, shell=True)

startCams("T1")
