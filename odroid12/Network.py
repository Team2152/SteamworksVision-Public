import multiprocessing;
import UDPSender;
import UDPReceiver;
import LightingHandler;
import sys;


# Use this as a global status variable for all threads attached to this process
STATUS = None;

''' Process method to be called as a target to the sender process
    UDPProcess :: str -> int -> int -> Queue -> Status -> () '''
def UDPProcess(host, sendPort, recvPort, dataQueue, status):
    log("Use [ENTER] to interrupt program");

	# Update status variable
    global STATUS;
    STATUS = status;

    # Start sender thread
    sender = UDPSender.UDPSender(host, sendPort, dataQueue);
    sender.start();

    # Start receiver thread
    receiver = UDPReceiver.UDPReceiver(recvPort);
    # Give a lighting handler set for cams 3 and 4 to the reciever
    receiver.dataHandlers.append(LightingHandler.Handler([3, 4]));
    receiver.start();
       
    # Wait for threads to stop
    while (sender.isAlive()): pass;
    while (receiver.isAlive()): pass;

    log("UDP Process Done.");

''' Start the UDP processes and return a reference to it
    startProcess :: str -> int -> int -> Queue-> Status -> Process '''
def startProcess(host, sendPort, recvPort, dataQueue, status):
    # Set debugging flag
    # multiprocessing.log_to_stderr(logging.DEBUG);
    
    # Start main process
    udpProcess = multiprocessing.Process(
        name="UDP_PROCESS",
        target=UDPProcess, 
        args=(host, sendPort, recvPort, dataQueue, status));
    udpProcess.start();

    return udpProcess;

''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: str -> () '''
def log(msg):
    print(msg);
    sys.stdout.flush();
