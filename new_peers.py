
import json
import socket

from threading import Thread

FILE = "peers.json"
PORT = 2019
MAX_CONS = 5
BUFFER_SIZE = 1

class PeerManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.stop = False
        
        #Create list of peer addresses
        self.peers = []

        self.client

        #Load peer data from json file
        try:
            file = open(FILE)
            peers_json = json.load(file)
            addrs = peers_json["peers"]
            for addr in addrs:
                self.add_peer(addr)
            file.close()
        except FileNotFoundError:
            file = open(FILE, "w")
            data = dict()
            data["peers"] = []
            json.dump(data, file)
            file.close()

        #Create server socket
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, PORT))
        

    def add_peer(self, addr):
        #! Make sure peer is not self
        if not (addr in self.peers):
            self.peers.append(addr)

    def run(self):
        #! Do more stuff here
        #
        #
        self.server.listen(MAX_CONS)
        while not self.stop:
            client, addr = self.server.accept()
            


class ClientThread(Thread):
    def __init__(self, addr):
        
