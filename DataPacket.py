import sys;

# Define packet variables here


class Param():

    def __init__(self, name, value):
        self.name = name;
        self.type = type(value);
        self.value = value;

    # Override native method 
    def __str__(self):
        return self.serialize();

    ''' Serializes self and returns as a string
        serialize :: string '''
    def serialize(self):
        # Define data structure for serialization
        data = ':' + str(self.type) + '|' + self.name + '|' + str(self.value) + ';';
        return data


class Packet(object):

    def __init__(self):
        # List of parameters that will be sent over a network
        self.params = [];
    
    ''' Method for sending parameters over a network.
        Should be overrided in derived class.
        @index : index of parameter
        sendData :: void '''
    def sendParam(self, index, data):
        # Override this
        return;

    ''' Sends self in serialized pieces
        send :: void '''
    def send(self):
        for i in range(len(self.params)):
            self.sendParam(i, self.params[i].serialize());
        
        
    
