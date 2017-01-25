import sys;

class Param():

    def __init__(self, name, value):
        self.name = name;
        self.type = type(value);
        self.value = value;

    ''' Set value if it is a valid type
        setValue :: void '''
    def setValue(self, value):
        if (type(value) == self.type):
            self.value = value;

    # Override native method 
    def __str__(self):
        return self.serialize();

    ''' Serializes self and returns as a string
        serialize :: str '''
    def serialize(self):
        # Define data structure for serialization

        data = ':' + str(self.type.__name__) + '|' + self.name + '|' + str(self.value) + ';';
        return data

# Implement this class for practical use
class Packet(object):

    def __init__(self):
        # List of parameters that will be sent over a network
        self.params = [];

    ''' Set corresponding parameter to a given value
        setParam :: void '''
    def setParam(self, paramName, value):
        for p in self.params:
            if (p.name == paramName):
                p.setValue(value);

    ''' Set corresponding parameter from a given packet
        setData :: void '''
    def setData(self, packet):
        for p in packet.params:
            self.setParam(p.name, p.value);

    ''' Method for sending parameters over a network.
        Should be implemented in derived class.
        @index : index of parameter
        sendData :: void '''
    def sendParam(self, index, data):
        raise NotImplementedError("Should implement for data transfer");
    
    ''' Sends self in serialized pieces
        send :: void '''
    def send(self):
        for i in range(len(self.params)):
            self.sendParam(i, self.params[i].serialize());
        
        
    
