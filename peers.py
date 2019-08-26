import json
import socket

PEER_DATA_FILE = "peers.json"

def create_peer_file():
    data = dict()
    data["known_peers"] = []
    data["current_peers"] = []
    with open(PEER_DATA_FILE, "w") as file:
        json.dump(data, file)


class PeerManager:
    def __init__(self):
        self.known_peers = list()
        self.current_peers = list()
        with open(PEER_DATA_FILE) as file:
            peers_json = json.load(file)
            self.known_peers = peers_json["known_peers"]
            self.current_peers = peers_json["current_peers"]
        self.hostname = socket.gethostname()
        self.inbox = list()
        self.outbox = list()

    
        
