import sys;
import UDPReceiver;
from subprocess import call 

RECORD_PATH = "home/odroid/recordings"
DEFAULT_RECORDING_DUR = 160;
TEST_RECORDING_DUR = 20;

TOPICS = [
    "/uc0/image_raw",
    "/uc1/image_raw",
    "/uc0_12/image_raw",
    "/uc1_12/image_raw"];

class Handler(UDPReceiver.DataHandler):

    def __init__(self):
        self.recording = False;

    def handle(self, data):
        camData = data.split(';');
        if ((not self.recording) and ('1' in camData[1])):
            self.recording = True;
            startRecording(camData[1], camData[2]);

''' Starts recording on all of the topics '''
def startRecording(cameraData, filename):
    log("Starting to record...");    
    
    # define the duration
    duration = DEFAULT_RECORDING_DUR;
    # enable test duration if camera data contains a 'T'
    if 'T'  in cameraData:
        duration = TEST_RECORDING_DUR;

    # define parameters for the following command
    parameters = "--duration=" + str(duration) + " -o " + filename;
    
    # define commands for shell
    cmd1 = "cd " + RECORD_PATH;
    cmd2 = "rosbag record " + TOPICS[0] + " " + TOPICS[1] + " " + TOPICS[2] + " " + TOPICS[3] + " " + parameters;
    
    # return status of command call
    return call(cmd1 + '''
    ''' + cmd2, shell=True);
    
''' Logs specified message for future debugging
    TODO: implement REAL logger here
    log :: str -> () '''
def log(msg):
    print(msg);
    sys.stdout.flush();
