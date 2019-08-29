import json
import socket

from threading import Thread

PORT = 2019
FILE = "peer_data.json"

class IncpOverTcp:
    def __init__(self):
        self.on = False

        #Maps to boolean of online status
        self.peers = dict()

        #List of dialogues this session
        #! Close dialogues when IncpOverTcp.stop is called
        self.dialogues = list()

        #Load peer data from json file
        try:
            file = open(FILE)
            print("Found peer data file {}".format(FILE))
            self.peers = json.load(file)
            file.close()
        except FileNotFoundError:
            print("Peer data file {} not found".format(FILE))
            print("Creating peer data file {}".format(File))
            file = open(FILE, "w")
            json.dump(self.peers, file)
            file.close()

    def answer_calls(self):
        while not self.on:
            client, (addr, port) = self.server.accept()
            print("Call from {} over port {}".format(addr, port))
            self.peers[addr] = True
            dialogue = Dialogue(addr, client)
            dialogue.start()
            self.dialogues.append(dialogue)

    def call(self, addr):
        print("Calling {}".format(addr))
        dialogue = Dialogue(addr)
        dialogue.start()
        self.dialogues.append(dialogue)

    def start(self):
        print("Starting INCP/TCP")
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, PORT))
        self.server.listen()
        self.on = True

        #Start answering calls on seperate thread
        self.answering_machine = Thread(self.answer_calls)
        print("Starting answering machine")
        self.answering_machine.start()

    def stop(self):
        print("Stopping INCP/TCP")
        self.on = False
        file = open(FILE, "w")
        json.dump(self.peers, file)
        file.close()



NO = b'\x00'[0]
YES = b'\x01'[0]
ACK = b'\x02'[0]
DEFAULT_GREETING = b'\x03'[0]
CHECK = b'\x03'[0]

class Dialogue(Thread):
    def __init__(self, addr, socket=None):
        Thread.__init__(self)
        self.addr = addr
        self.socket = None
        #This node is the caller if no socket is provided
        self.am_caller = (socket == None)
        self.greeting = DEFAULT_GREETING

    def set_greeting(self, greeting):
        self.greeting = greeting

    def run(self):
        if self.am_caller:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.addr, PORT))
            print("Greeting {}".format(self.addr))
            self.socket.send(self.greeting)
            #Assumes default greeting
            #! Stop assuming default greeting
            resp = self.socket.recv(1)
            if resp == ACK:
                print("{} acknowledged greeting".format(self.addr))
        else:
            msg = self.socket.recv(1)
            if msg == CHECK:
                print("Check from {}".format(self.addr))
                self.socket.send(ACK)
                










            