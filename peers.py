import json
import socket
from threading import Thread

PEERS_DATA_FILE = "peers.json"
PORT = 2019
MAX_CONNECTIONS = 5
BUFFER_SIZE = 1

COMCODES = {
    "on": b'\x01',
    "off": b'\x00',
    "ack": b'\x02'
}


class Peer:
    def __init__(self, addr):
        self.addr = addr
        self.is_on = False

    def notify_online(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.addr, PORT))
        sock.send(COMCODES["on"])
        sock.

    def notify_offline(self):
        pass

    def acknowledge(self):
        pass


class PeerManager:
    def __init__(self):
        #Create list of peer objects
        self.peers = []

        #Load peer data from json file
        try:
            file = open(PEERS_DATA_FILE)
            peers_json = json.load(file)
            addrs = peers_json["peers"]
            for addr in addrs:
                self.add_peer(addr)
            file.close()
        except FileNotFoundError:
            file = open(PEERS_DATA_FILE, "w")
            data = dict()
            data["peers"] = []
            json.dump(data, file)
            file.close()

        #Create server socket
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, PORT))
        self.server.listen(MAX_CONNECTIONS)

        #Notify known peers
        if len(self.peers) > 0:
            for peer in self.peers:
                peer.notify_online()


    def add_peer(self, addr):
        self.peers.append(Peer(addr))
        

    
        
