#!/usr/bin/env python
import Network;
import logging;
import socket, sys, os, traceback, logging;
import multiprocessing;
import DataPacket;
import threading;
import time;
from Utils import Status;

'''
    Sends data from queue to target ip on specified port
    via UDP. Data packet will be sent on a set time interval.
    Use queue ONLY for commands 
    Handles all networking procedures. 
    
    Press [ENTER] to interrupt program safely
'''

# logging.basicConfig(filename="/home/odroid/catkin_ws/log/autoRecord.log", filemode="w", level=logging.DEBUG);

CLOCK_DELAY = 0.1;

class DataHandler(object):
    def handle(self, data):
        return;

# Handles udp networking
class UDPReceiver(threading.Thread):     
        
    def __init__(self, port):
        threading.Thread.__init__(self);

        # Parameters for receiving via udp
        self.port = port;
        self.dataHandlers = [];
        
        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
    ''' Sends data to host
        sendData :: Packet -> () '''
    def receiveData(self):
        #log("Receiving Data: ");
        try:
            data, addr = self.socket.recvfrom(1024);
            return data

        except socket.error:
            #log("Data Receive Failed");
            #traceback.print_exc();
            return None;
    
    ''' Sender thread loop
        run :: () -> () '''
    def run(self):
        self.socket.setblocking(0);
        # Bind to port
        self.bind();
        
        log("Ready to receive data. (:");        
        # Network loop
        while (not Network.STATUS.isStopped()):
             data = self.receiveData();
             if (data != None):        
                log("Something received." + str(data));
                for handler in self.dataHandlers:
                    handler.handle(data);
             time.sleep(CLOCK_DELAY);
        # Close socket
        self.close();

    ''' Binds socket to udp port and return if successful
        bind :: () -> bool '''    
    def bind(self):
        log("Binding to port " + str(self.port) + "...");
        try :
            # Attempt to bind to port
            self.socket.bind(('', self.port));
            return True;
        except socket.error:
            log("Binding failed to port: " + str(self.port));
            traceback.print_exc();
            return False;

    ''' Closes socket for safety
        close :: () -> () '''
    def close(self):
        log("Closing receiver socket...");
        self.socket.close();
       
       
''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: str -> () '''
def log(msg):
    logging.debug(msg);
    sys.stdout.flush();
