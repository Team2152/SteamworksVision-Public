#!/usr/bin/env python
import socket, sys, os, traceback, logging;
import Network;
import DataPacket;
import threading;

from Utils import Status;

'''
    Sends data from queue to target ip on specified port
    via UDP. Data packet will be sent on a set time interval.
    Use queue ONLY for commands 
    Handles all networking procedures. 
    
    Press [ENTER] to interrupt program safely
'''

# Handles udp networking
class UDPSender(threading.Thread):     

    def __init__(self, host, port, dataQueue):
        threading.Thread.__init__(self);

        # Parameters for sending via udp
        self.host = host;
        self.port = port;

        self.dataQueue = dataQueue;

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
        # Send count for debugging        
        self.sendCount = 0;
        
    ''' Sends data to host
        sendData :: Packet -> () '''
    def sendData(self, data):
        self.sendCount += 1;
        log("Sending Data to " + self.host + "... Send Count: " + str(self.sendCount));
        try:
            self.socket.sendto(data, (self.host, self.port));

        except:
            log("Data Transfer Failed");
            traceback.print_exc();
    
    ''' Sender thread loop
        run :: () -> () '''
    def run(self):
        # Bind to port
        self.bind();
        
        log("Ready to send data. (:");        

        # Sending loop
        while (not Network.STATUS.isStopped()):
            # Check for queue packets
            while (not self.dataQueue.empty()): 
                # Pop data from shared queue
                data = self.dataQueue.get();
                
                if (Network.STATUS.isRunning()):
                    # Acknowledge data
                    if (isinstance(data, DataPacket.Packet)):
                        # Send serialized data
                        self.sendData(data.serialize());
                    else:
                        log("Not a valid object type");

        # Close socket
        self.close();

    ''' Binds socket to udp port and return if successful
        bind :: () -> bool '''    
    def bind(self):
        log("Binding to port " + str(self.port) + "...");
        try :
            self.socket.bind(('', self.port));
            return True;

        except socket.error:
            log("Binding failed to port: " + str(self.port));
            traceback.print_exc();
            return False;

    ''' Closes socket for safety
        close :: () -> () '''
    def close(self):
        log("Closing sender socket...");
        self.socket.close();
 

''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: str -> () '''
def log(msg):
    print(msg);
    sys.stdout.flush();

