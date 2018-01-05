#!/usr/bin/env python
import multiprocessing;
import sys;
import Network;
import UDPSender;
import UDPReceiver;
import runScript;
from DataPacket import *;

import Utils;
from Utils import Status;

# Program status flag to be shared among all processes
STATUS = Status(Status.RUNNING);

# Queue for data to go to sender
DATA_QUEUE = multiprocessing.Queue();

# Network information
UDP_SEND_PORT      = 5800;          #Send to port on to Roborio
TARGET_IP     = "10.21.52.2";  #Send to ip address of the Roborio

UDP_RECV_PORT = 5810;          #Receive port (roborio sends cam settings)

# Stops the program on key press
class Reaper(Utils.KeyListener):
    def onStop(self):
        stop();

def main():
 
    # Start the network process (sender and receiver)
    networkProcess = Network.startProcess(TARGET_IP, UDP_SEND_PORT, UDP_RECV_PORT, DATA_QUEUE, STATUS);
    
    # Start vision processes
    boilerVisionProcess = None;
    pegVisionProcess = multiprocessing.Process(target=runScript.run, args=(DATA_QUEUE, STATUS)).start();
    
    # Start example / dummmy process    
    # dummyProcess = multiprocessing.Process(target=DummyProcess, args=(DATA_QUEUE, STATUS)).start();

    # Wait for status to signal stop
    while (not STATUS.isStopped()): pass;
    
    # Program will not end until all processes are terminated

''' Stops the program by setting the shared status variable
    stop :: () -> () '''
def stop():
    log("Program stopping...");

    global STATUS;
    STATUS.setStatus(Status.STOPPED);

    log("Use [CTL-C] to terminate runScript.py process.");

''' Set global variables from program arguments
    setArgs :: () -> () '''
def setArgs():
    global TARGET_IP, UDP_PORT;
    if (len(sys.argv) >=  3):
        TARGET_IP = sys.argv[1];
        UDP_PORT  = int(sys.argv[2]);
    else:
        log("NOT ENOUGH ARGUMENTS!!!");
        log("USE: Core.py [TARGET_IP] [UDP_PORT]");
        sys.exit(0);

''' Logs the specified message to the terminal
    log :: str -> () '''
def log(msg):
    print(msg);

if __name__ == "__main__":
    # setArgs();
    # start reaper when the core is standalone
    Reaper().start();
    main();
    




