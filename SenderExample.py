import sys;
import DataPacket;
import UDPSender;
import multiprocessing;
import time;

# Create a template of the data that will be sent over the network
dataPacket = DataPacket.Packet();
dataPacket.params = [
    DataPacket.Param("Running", True)
]


# Call @startProcess([HOST_IP], [UDP_PORT], [DATA_TEMPLATE]) 
sender = UDPSender.startProcess("localhost", 56081, dataPacket);

time.sleep(2);

# Make changes to data
dataPacket.setParam("Running", False);

# Call on update to data
UDPSender.sendData(dataPacket);

time.sleep(2);

# Create new data signature
dataPacket.params = [
    DataPacket.Param("New Var 1", 2L),
    DataPacket.Param("New var 2", 3L)
]

# Command process to use the next packet as the signature
UDPSender.commandProcess(UDPSender.Command.CHANGE_SIG);

# Send new signature packet
UDPSender.sendData(dataPacket);

# Program waits for sender process to exit (PRESS ENTER)

# Can safely stop process manually if need be with:
# UDPSender.stopProcess();

