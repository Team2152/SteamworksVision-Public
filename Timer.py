import time;

# Simple timer class
class Timer(object):

    ''' @duration:  duration of timer in seconds
        @autoReset: whether to reset after it is done '''
    def __init__(self, duration, autoReset):
        self.duration = float(duration);
        self.autoReset = autoReset;
        self.startTime = 0.0;
    
    ''' Start timer (set @startTime variable)
        start :: void '''
    def start(self):
        self.startTime = time.time();

    ''' Gets progress of timer from (0.0 - 1.0)
        getProgress :: float '''
    def getProgress(self):
        currentTime = time.time();
        elapse = currentTime - self.startTime;
        if (self.autoReset and (elapse >= self.duration)):
            # Recalculate @startTime and compensate for
            # extra time spent from last call to now
            self.startTime = currentTime - elapse % self.duration;

        return elapse / self.duration;        

    ''' Checks if timer is finished
        finished :: bool '''
    def finished(self):
        return (self.getProgress() >= 1);
        
