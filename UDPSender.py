import socket, sys, os, traceback, logging;
import multiprocessing;
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

# Status of program
STATUS = None;

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
        
        log("Waiting for input data...");        

        # Sending loop
        while (not STATUS.isStatus(Status.STOPPED)):
            # Check for queue packets
            while (not self.dataQueue.empty()): 
                # Pop data from shared queue
                data = self.dataQueue.get();
                
                if (STATUS.isStatus(Status.RUNNING)):
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
        log("Closing socket...");
        self.socket.close();

''' Process method to be called as a target to the sender process
    UDPProcess :: str -> int -> Queue -> () '''
def UDPProcess(host, port, dataQueue, status):
    log("Use [ENTER] to interrupt program");

    global STATUS;
    STATUS = status;

    # Start sender thread
    sender = UDPSender(host, port, dataQueue);
    sender.start();
       
    while(not STATUS.isStatus(Status.STOPPED)): pass;

    while (sender.isAlive()): pass;

    log("UDP Sender Done.");

''' Start the UDPSender process and return a reference to it
    Give host ip, udp port, and template packet
    startProcess :: str -> int -> Process '''
def startProcess(host, port, dataQueue, status):
    # Set debugging flag
    # multiprocessing.log_to_stderr(logging.DEBUG);
    
    # Start main process
    udpProcess = multiprocessing.Process(
        name="UDP_SENDER",
        target=UDPProcess, 
        args=(host, port, dataQueue, status));
    udpProcess.start();

    return udpProcess;  

''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: str -> () '''
def log(msg):
    print(msg);
    sys.stdout.flush();

