import socket, sys, os, traceback;
from multiprocessing import Queue;
from multiprocessing import Process;
import DataPacket;
import threading;
import Timer;

'''
    Usage: python UDPSender.py [HOST_IP] [UDP_PORT]

    Sends data from queue to target ip on specified port
    via UDP. Handles all networking procedures. 
    
    Press [ENTER] to interrupt program safely
'''

# Target udp port and host ip (retreive from arguments)
# sys.argv[0] is program file name
UDP_PORT = int(sys.argv[2]);
HOST_IP  = sys.argv[1];

# Status of program
RUNNING = True;

# Threads
UDP_SENDER   = None;
KEY_LISTENER = None;

# Data Queue for sending
DATA_QUEUE = Queue();

# Data packet for runtime communication
# Define robot parameters to be sent here
PACKET = DataPacket.Packet();
PACKET.params = [
DataPacket.Param("Running", True),
DataPacket.Param("Move X",  0.0 ),
DataPacket.Param("Move Y",  0.0 )
];


# Handles udp networking
class UdpSender(threading.Thread):

    # Nested packet class (extended from @DataPacket.Packet)
    class RobotPacket(DataPacket.Packet):
        def __init__(self, udpSender):
            super(UdpSender.RobotPacket, self).__init__();
            self.udpSender = udpSender;
 
        ''' Sends data (overrided method)
            sendData :: void '''
        def sendParam(self, index, data):
            self.udpSender.sendData(data);
            log("-> Chunk " + 
                str(index + 1) + " of " + 
                str(len(self.params)) + " : ('" + 
                str(data) + "')");        

    def __init__(self, host, port, packet):
        threading.Thread.__init__(self);

        # Flag for thread loop 
        self.running = False;

        # Parameters for sending via udp
        self.host = host;
        self.port = port;

        # Data packet that will be iteratively sent
        self.packet = self.RobotPacket(self);
        self.packet.params = packet.params;

        # Create self-resetting timer
        self.sendTimer = Timer.Timer(2, True);
        self.sendTimer.start();

        # Inititialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
        # Send count for debugging        
        self.sendCount = 0;
        
    ''' Sends data to host
        sendData :: void '''
    def sendData(self, data):
        self.sendCount += 1;
        log("Sending Data... Send Count: " + str(self.sendCount));
        try:
            self.socket.sendto(data, (self.host, self.port));

        except:
            log("Data Transfer Failed");
            traceback.print_exc();

    ''' Sender thread loop
        run :: void '''
    def run(self):
        global DATA_QUEUE
        self.running = True;

        # Bind to port
        self.bind();
        
        log("Waiting for input data...");        

        # Sending loop
        while (self.running):

            # Check for queue packets
            while (not DATA_QUEUE.empty()):
                # Send as long as the queue is not empty 
                self.sendData(DATA_QUEUE.get());

            # Send every timer cycle
            if (self.sendTimer.finished()):
                log("\nSending Parameter Data Packet...");        
                # Send default data packet
                self.packet.send();
        
        # Close socket
        self.close();

    ''' Binds socket to udp port and return if successful
        bind :: bool '''    
    def bind(self):
        log("Binding to port " + str(self.port) + "...");
        try :
            self.socket.bind(('', self.port));
            return True;

        except socket.error:
            log("Binding failed to port: " + str(self.port));
            traceback.print_exc();
            return False;

    ''' Stops thread and closes thread
        stop :: void '''
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
    global UDP_SENDER, KEY_LISTENER;    

    valid = validArguments();
    if (not valid):
        log("Not valid arguments.");
        log("python UDPSender.py [HOST_IP] [UDP_PORT]");
        os._exit(0);

    log ("Use [ENTER] to interrupt program");

    # Start program threads
    UDP_SENDER = UdpSender(HOST_IP, UDP_PORT, PACKET);
    KEY_LISTENER = KeyListener();

    UDP_SENDER.start();
    KEY_LISTENER.start();

    while(RUNNING):
        # Do nothing
        pass;
    
    # Stop program
    stop();

''' Check if arguments are valid for use
    validArguments :: bool '''
def validArguments():

    if (not isinstance(UDP_PORT, int)): return False;
    if (not isinstance(HOST_IP,  str)): return False;
    
    return True;

''' Adds data to queue to be sent by sender thread
    sendData :: void '''
def sendData(data):
    global DATA_QUEUE
    DATA_QUEUE.put(data);

''' Stops program 
    stop :: void '''
def stop():
    UDP_SENDER.stop();

    while UDP_SENDER.isAlive():
        # Wait for thread death
        pass;

    os._exit(0);    

''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: void '''
def log(msg):
    print(msg);


# Start point of program
if __name__ == '__main__':
    main();
