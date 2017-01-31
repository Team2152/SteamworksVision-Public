import multiprocessing;
import threading;
import time;

class KeyListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
    
    ''' Runs when the thread self-stops and should be overriden
        onStop :: () -> () '''
    def onStop(self):
        return;

    ''' Waits for the [ENTER] key then calls @onStop method
        run :: () -> () '''
    def run(self):
        raw_input();
        self.onStop();

class Status():
    STOPPED = 0;
    RUNNING = 1;
    STANDBY = 2;

    def __init__(self, status):
        self.sharedObject = multiprocessing.Value('i', status);

    def setStatus(self, status):
        self.sharedObject.value = status;

    def isStatus(self, status):
        return (self.sharedObject.value == status);

    def isStopped(self):
        return self.isStatus(self.STOPPED);

    def isRunning(self):
        return self.isStatus(self.RUNNING);

    def isStandby(self):
        return self.isStatus(self.STANDBY);

    def __str__(self):
        return str(self.sharedObject.value);

