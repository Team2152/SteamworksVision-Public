import sys;
import DataPacket;
import UDPSender;
import multiprocessing;

# Create a template of the data that will be sent over the network
dataPacket = DataPacket.Packet();
dataPacket.params = [
    DataPacket.Param("Running", True)
]


# Call @startProcess([HOST_IP], [UDP_PORT], [DATA_TEMPLATE]) 
sender = UDPSender.startProcess("localhost", 56081, dataPacket);

# Make changes to data
dataPacket.setParam("Running", False);

# Call on update to data
UDPSender.sendData(dataPacket);



