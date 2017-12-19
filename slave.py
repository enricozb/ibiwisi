from capture import capture
from connection import Connection

class Slave:
    def __init__(self, port):
        self.connection = Connection(port)

    def set_master(self, addr):
        self.connection.set_sink(addr)

    def run(self):
        while True:
            self.connection.send(capture())
            self.connection.recv()

