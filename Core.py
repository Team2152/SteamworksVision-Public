import multiprocessing;
import sys;
import UDPSender;
import runScript;
from DataPacket import *;

import Utils;
from Utils import Status;

# Program status flag to be shared among all processes
STATUS = Status(Status.RUNNING);

# Queue for data to go to sender
DATA_QUEUE = multiprocessing.Queue();

# Network information
UDP_PORT  = 5800;
TARGET_IP = "roboRio-2152-FRC.local";

# Stops the program on key press
class Reaper(Utils.KeyListener):
    def onStop(self):
        stop();

def main():

    # Start program reaper to kill program with key press (ENTER)
    reaper = Reaper();
    reaper.start();
    
    # Start the sender process
    senderProcess = UDPSender.startProcess(TARGET_IP, UDP_PORT, DATA_QUEUE, STATUS);

    # Start vision processes
    boilerVisionProcess = None;
    pegVisionProcess = multiprocessing.Process(target=runScript.run, args=(DATA_QUEUE, STATUS)).start();
    
    # Start example / dummmy process    
    # dummyProcess = multiprocessing.Process(target=DummyProcess, args=(DATA_QUEUE, STATUS)).start();

    # Wait for status to signal stop
    while (not STATUS.isStopped()): pass;
    
''' Stops the program by setting the shared status variable
    stop :: () -> () '''
def stop():
    log("Program stopping...");

    global STATUS;
    STATUS.setStatus(Status.STOPPED);

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
    setArgs();
    main();
    




