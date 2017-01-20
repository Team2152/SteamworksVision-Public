import socket, sys, os, traceback;
from multiprocessing import Queue;
from multiprocessing import Process;
import threading;
import time;

'''
    Sends data from queue to target ip on specified port
    via UDP. Handles all networking procedures. 
    
    Press [ENTER] to interrupt program safely
'''

# Target udp port and host ip
UDP_PORT = 5801;
HOST_IP  = "10.151.106.190";

# Status of program
RUNNING = True;

# Threads
UDP_SENDER   = None;
KEY_LISTENER = None;

# Handles udp networking
class UdpSender(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self);
        
        self.running = False;

        self.host = host;
        self.port = port;

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
    ''' Sends data to host
        sendData :: void '''
    def sendData(self, data):
        self.socket.sendto(data, (self.host, self.port));

    ''' Sender thread loop
        run :: void '''
    def run(self):
        self.running = True
        self.bind();
        
        # Sending loop
        while(self.running):
            log("Sending Data Packet...");
            try:
                data = "WHAT UP";
                self.sendData(data);

            except:
                log("Data Transfer failed");
                traceback.print_exc();
            time.sleep(1);
        
        # Close socket
        self.close();

    ''' Binds socket to udp port and return if successful
        bind :: bool '''    
    def bind(self):
        try :
            self.socket.bind(('', self.port));
            return True;

        except socket.error:
            log("Binding failed to port: " + self.port);
            traceback.print_exc();
            return False;
    
    ''' Stops thread and closes thread
        stpp :: void '''
    def stop(self):
        self.running = False;

    ''' Closes socket for safety
        close :: void '''
    def close(self):
        log("Closing socket...");
        self.socket.close();

# Handles input data
class KeyListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        
    ''' Listener thread loop
        run :: void '''
    def run(self):
        global RUNNING

        while (RUNNING):
            # Wait for any input (blocks thread)
            raw_input();
            
            # Set @RUNNING flag appropriately
            RUNNING = False;

            log("Program Stopping...");

''' Main method
    main :: void '''
def main():

    log ("Use [ENTER] to interrupt program");

    global UDP_SENDER, KEY_LISTENER;    

    # Start program threads
    UDP_SENDER = UdpSender(HOST_IP, UDP_PORT);
    KEY_LISTENER = KeyListener();

    UDP_SENDER.start();
    KEY_LISTENER.start();

    while(RUNNING):
        # Do nothing
        pass;
    
    # Stop program
    stop();


''' Stops program 
    stop :: void '''
def stop():
    UDP_SENDER.stop();

    while UDP_SENDER.isAlive():
        # Wait for thread death
        pass;

    os._exit(0);    

''' Logs specified message for future debugging
    log :: void '''
def log(msg):
    print(msg);


# Start point of program
if __name__ == '__main__':
    main();
