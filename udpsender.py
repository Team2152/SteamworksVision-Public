import socket, sys, os, traceback;
from multiprocessing import Queue;
from multiprocessing import Process;
import threading;
import time;


# Target udp port and host ip
UDP_PORT = 5801;
HOST_IP =  "10.151.106.190";


class UdpSender(threading.Thread):
    
    def __init__(self, host, port):
        threading.Thread.__init__(self);
        
        self.host = host;
        self.port = port;

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
    # sends data to host
    # sendData :: void
    def sendData(self, data):
        self.socket.sendto(data, (self.host, self.port));

    # main thread loop
    # run :: void
    def run(self):
        self.bind();
        
        loopCount = 10;
        while(True):
            print("Sending Data Packet...");
            try:
                data = "WHAT UP";
                self.sendData(data);

            except:
                print "Data Transfer failed";
                traceback.print_exc();
            time.sleep(1);

            loopCount -= 1;
            if (loopCount <= 0): break;

        self.close();

    # bind socket to udp port and return if successful
    # bind :: bool    
    def bind(self):
        try :
            self.socket.bind(('', self.port));
            return True;

        except socket.error:
            print("Binding failed to port: " + self.port);
            traceback.print_exc();
            return False;
    
    # closes socket and releases port
    # close :: void
    def close(self):
        self.socket.close();

# start point of program
if __name__ == '__main__':
    UdpSender(HOST_IP, UDP_PORT).run();
