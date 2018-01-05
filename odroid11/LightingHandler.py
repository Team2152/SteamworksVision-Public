import sys;
import UDPReceiver;
from subprocess import call;

class Handler(UDPReceiver.DataHandler):
    CAM_NORMAL = "0";
    CAM_DARK   = "1";    
    
    #################################################################
    #                  USB3.0    USB2.0       USB3.0     USB2.0     #
    #                  Video1    Video0       Video1     Video0     #
    # cams[0] = "CS",  [1]=Peg,  [2]=Boiler,  [3]=Rope,  [4]=Intake #
    #################################################################   
    
    ''' camIds is an array of indexes for the cameras as they are positioned in
    the data string '''
    def __init__(self, camIds):
        # create a camera dictionary as {cameraId(int): cameraValue(CAM_NORMAL, CAM_DARK)}        
        self.cams = {};
        # make dictionary entries for each given camera id
        for camId in camIds:
            self.cams[camId] = self.CAM_NORMAL;
        
    ''' Handles data as it is received from the UDPReceiver '''
    def handle(self, data):
        camData = data.split(';');
        
        # cycle through all the keys or ids in the camera dictionary
        camIds = self.cams.keys();
        for camIndex in range(len(camIds)):
            # get the id
            camId = camIds[camIndex];
            # get the data with key            
            data = camData[camId];
            # check if a change is requested            
            if (self.cams[camId] != data):
                # apply requested change
                self.applyLighting(camIndex, data);
                self.cams[camId] = data; 
            
    def applyLighting(self, camId, data):
        if (data == self.CAM_NORMAL): makeNormal(camId);
        if (data == self.CAM_DARK): makeDark(camId);

''' Makes a given camera darker '''
def makeDark(cam):
   log("Making Dark Video " + str(cam));
   cmd1 = "v4l2-ctl -d /dev/video" + str(cam) + " -c brightness=0 -c contrast=40 -c saturation=154 -c hue=0 -c white_balance_automatic=0 -c auto_exposure=1 -c exposure=5 -c gain_automatic=0 -c gain=20 -c sharpness=0" 
   cmd2 = "v4l2-ctl -d /dev/video" + str(cam) + " -c exposure=5 -c gain=20"
   call(cmd1, shell=True)
   call(cmd2, shell=True)

''' Makes a given camera normal '''
def makeNormal(cam):
   log("Making Normal Video " + str(cam));
   cmd1 = "v4l2-ctl -d /dev/video" + str(cam) + " -c brightness=0 -c contrast=32 -c saturation=64 -c hue=0 -c white_balance_automatic=1 -c auto_exposure=0 -c exposure=63 -c gain_automatic=1 -c gain=4 -c sharpness=10"
   cmd2 = "v4l2-ctl -d /dev/video" + str(cam) + " -c exposure=63 -c gain=4" 
   call(cmd1, shell=True)
   call(cmd2, shell=True)
   
''' Logs the specified message to the terminal
    log :: str -> () '''
def log(msg):
    print(msg);
    sys.stdout.flush();
