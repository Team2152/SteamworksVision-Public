from networktables import NetworkTables
import time

ip = "10.153.102.5"
NetworkTables.initialize(server=ip)
ta = NetworkTables.getTable("table")

i = 0
while(i < 10):
    ta.putNumber("a", 343)
    time.sleep(1)
    print(i)
    i+=1


