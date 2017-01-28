import socket, sys, os, traceback, logging;
import multiprocessing;
import DataPacket;
import threading;
import Timer;

'''
    Usage: python UDPSender.py [HOST_IP] [UDP_PORT]

    Sends data from queue to target ip on specified port
    via UDP. Data packet will be sent on a set time interval.
    Use queue ONLY for commands 
    Handles all networking procedures. 
    
    Press [ENTER] to interrupt program safely
'''

# Whether code is running as a standalone
IS_STANDALONE = False;

# Target udp port and host ip
IP_PORT = 0;
HOST_IP = "";

# Status of program
RUNNING = True;

# Threads
UDP_SENDER     = None;
INPUT_LISTENER = None;

# Data Queue for sending
DATA_QUEUE = None;

# Commands for @UdpSender to execute
class Command():
    NONE       = 0;
    STOP       = 1;
        
    def __init__(self, command):
        self.command = command;

    def isCommand(self, command):
        return (self.command == command);


# Handles udp networking
class UDPSender(threading.Thread):     

    def __init__(self, host, port):
        threading.Thread.__init__(self);
        
        # Flag for thread loop 
        self.running = False;

        # Parameters for sending via udp
        self.host = host;
        self.port = port;

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        
        # Send count for debugging        
        self.sendCount = 0;
        
    ''' Sends data to host
        sendData :: void '''
    def sendData(self, data):
        self.sendCount += 1;
        log("Sending Data to " + self.host + "... Send Count: " + str(self.sendCount));
        try:
            self.socket.sendto(data, (self.host, self.port));

        except:
            log("Data Transfer Failed");
            traceback.print_exc();

    def executeCommand(self, cmd):
        global RUNNING;

        cmdID = cmd.command;
        log("Executing incoming command...  CMD_CODE: " + str(cmdID));    

        # Execute by specified command id
        if (cmdID == Command.STOP):
            RUNNING = False;
        
    
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
                # Pop data from shared queue
                data = DATA_QUEUE.get();

                # Acknowledge data
                if (isinstance(data, DataPacket.Packet)):
                    # Send serialized data
                    self.sendData(data.serialize());

                elif (isinstance(data, Command)):
                    # Execute command if given
                    self.executeCommand(data);

                else:
                    log("Not a valid object type");

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
# This MUST be threaded on the main process because
# of call to @raw_input()
class InputListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        
    ''' Listener thread loop
        run :: void '''
    def run(self):
        global RUNNING;

        while (RUNNING):
            # Wait for any input (blocks thread)
            raw_input();
            
            if (IS_STANDALONE):
                # Set @RUNNING flag appropriately
                RUNNING = False;
                break;
            else:
                stopProcess();
                break;

        log("Key listener dead.");

''' Process method to be called as a target to the sender process
    UDPProcess :: void '''
def UDPProcess(host, port, signature, dataQueue):
    global UDP_PORT, HOST_IP, DATA_QUEUE;
    
    # Set globals to arguments
    UDP_PORT       = port;
    HOST_IP        = host;
    DATA_QUEUE     = dataQueue;

    main();

    log("Sender Process Ended.");

''' Main method
    main :: void '''
def main():
    global UDP_SENDER, INPUT_LISTENER;    
    
    # Check validity of arguments
    valid = validArguments();
    if (not valid):
        log("Not valid arguments.");
        log("python UDPSender.py [HOST_IP] [UDP_PORT]");
        return;

    log("Use [ENTER] to interrupt program");

    # Start program threads
    UDP_SENDER = UDPSender(HOST_IP, UDP_PORT);
    UDP_SENDER.start();
    
    # Create input thread when programs runs as a standalone
    if (IS_STANDALONE):
        INPUT_LISTENER = InputListener();
        INPUT_LISTENER.start();

    while(RUNNING):
        # Do nothing
        pass;

    # Stop program
    stop();

    return;

''' Check if arguments are valid for use
    validArguments :: bool '''
def validArguments():

    if (not isinstance(HOST_IP,  str)): return False; 

    # Check if port is a number
    global UDP_PORT;
    try:
        UDP_PORT = int(UDP_PORT)    
    except ValueError:
        return False;

    return True;

''' Adds data to queue to be sent by sender thread
    sendData :: void '''
def sendData(data):
    global DATA_QUEUE;

    if (isinstance(data, DataPacket.Packet)):
        DATA_QUEUE.put(data);
    else:
        log("Can only send instances of @DataPacket.Packet");

''' Commands the sender process with specified command (ID)
    commandProcess :: void '''
def commandProcess(command):
    global DATA_QUEUE;

    DATA_QUEUE.put(Command(command));

''' Start the UDPSender process and return a reference to it
    Give host ip, udp port, and template packet
    startProcess :: Process '''
def startProcess(host, port, packet):
    # Set debugging flag
    # multiprocessing.log_to_stderr(logging.DEBUG);
    
    # Create new queue for data transfer between processes
    global DATA_QUEUE;
    DATA_QUEUE = multiprocessing.Queue();
    
    # Start main process
    udpProcess = multiprocessing.Process(
        name="UDP_SENDER",
        target=UDPProcess, 
        args=(host, port, packet, DATA_QUEUE));
    udpProcess.start();

    # Start new thread from caller's process
    # This will be used to end the main process
    global INPUT_LISTENER;
    INPUT_LISTENER = InputListener();
    INPUT_LISTENER.start();

    return udpProcess;  

''' Stops the sender process from another process
    stopProcess :: void '''
def stopProcess():
    log("Sending stop command to UDPSender process...");

    # Send stop command to @UDPSender through shared queue
    commandProcess(Command.STOP);

''' Stops program 
    stop :: void '''
def stop():
    UDP_SENDER.stop();

    while UDP_SENDER.isAlive():
        # Wait for thread death
        pass;    

''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: void '''
def log(msg):
    print(msg);
    sys.stdout.flush();


# Start point of program
if __name__ == '__main__':
    # Update standalone flag    
    IS_STANDALONE = True;

    UDPProcess(sys.argv[1], sys.argv[2]);
