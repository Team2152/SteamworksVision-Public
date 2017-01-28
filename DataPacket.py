import sys;

class Param():

    def __init__(self, name, value):
        self.name = name;
        self.value = value;

    ''' Set value if it is a valid type
        setValue :: void '''
    def setValue(self, value):
        self.value = value;

    # Override native method 
    def __str__(self):
        return self.serialize();

    ''' Serializes self and returns as a string
        serialize :: str '''
    def serialize(self):
        # Define data structure for serialization
        data = self.name + '=' + str(self.value);
        return data;

# %item:name1=value1,name2=value2,...;
# Implement this class for practical use
class Packet(object):
    # Class used as an enumeration
    class Item():
        PEG    = "peg";
        BOILER = "boiler";

    def __init__(self):
        # List of parameters that will be sent over a network;
        self.params = [];
        self.item = Item.PEG;

    ''' Set corresponding parameter to a given value
        setParam :: void '''
    def setParam(self, paramName, value):
        for p in self.params:
            if (p.name == paramName):
                p.setValue(value);
    
    ''' Set item to specified value
        setItem :: void '''
    def setItem(self, item):
        self.item = item;

    ''' Set corresponding parameter from a given packet
        setData :: void '''
    def setData(self, packet):
        for p in packet.params:
            self.setParam(p.name, p.value);
    
    ''' Serialize packet into string
        serialize :: str '''
    def serialize(self):
        data = "";
        length = len(self.params);
        for i in range(length):
            data = data + p.serialize();
            if (i < length - 1) data = data + ",";
        return "%" + self.item + ":" + data + ";";
            
               
