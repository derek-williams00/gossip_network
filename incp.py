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
            print("<INCP> Found peer data file {}".format(FILE))
            self.peers = json.load(file)
            file.close()
        except FileNotFoundError:
            print("<INCP> Peer data file {} not found".format(FILE))
            print("<INCP> Creating peer data file {}".format(FILE))
            file = open(FILE, "w")
            json.dump(self.peers, file)
            file.close()

        #Create answering machine
        self.answering_machine = AnsweringMachine(self)

    def call(self, addr):
        print("<INCP> Calling {}".format(addr))
        dialogue = Dialogue(addr)
        dialogue.start()
        self.dialogues.append(dialogue)

    def start(self):
        print("<INCP> Starting INCP/TCP")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', PORT))
        self.server.listen()
        self.on = True
        #Start answering calls on seperate thread
        self.answering_machine.start()

    def stop(self):
        print("<INCP> Stopping INCP/TCP")
        self.on = False

        #Close all remaining dialogues and sockets
        for dialogue in self.dialogues:
                dialogue.close()

        #Filter remaining dialogues until all have closed
        while len(self.dialogues) > 0:
            remaining = []
            for dialogue in self.dialogues:
                if not dialogue.closed:
                    remaining.append(dialogue)
            self.dialogues = remaining
            
        #Save current peer addresses
        file = open(FILE, "w")
        json.dump(self.peers, file)
        file.close()



class AnsweringMachine(Thread):
    def __init__(self, com):
        Thread.__init__(self)
        self.com = com

    def run(self):
        print("<INCP> Starting answering machine")
        while self.com.on:
            client, (addr, port) = self.com.server.accept()
            print("<INCP> Call from {} over port {}".format(addr, port))
            self.com.peers[addr] = True
            dialogue = Dialogue(addr, client)
            dialogue.start()
            self.com.dialogues.append(dialogue)



NO = b'\x00'
YES = b'\x01'
ACK = b'\x02'
DEFAULT_GREETING = b'\x03'
CHECK = b'\x03'


class Dialogue(Thread):
    def __init__(self, addr, socket=None):
        Thread.__init__(self)
        self.addr = addr
        self.socket = socket
        self.am_caller = False
        self.greeting = None
        self.closed = False
        #This node is the caller if no socket is provided
        if self.socket == None:
            print("<INCP> Starting dialogue with {}".format(self.addr))
            self.am_caller = True
            self.greeting = DEFAULT_GREETING
        else:
            print("<INCP> Dialogue started by {}".format(self.addr))
        
 
    def set_greeting(self, greeting):
        self.greeting = greeting

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.closed = True

    def run(self):
        if self.am_caller:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.addr, PORT))
            print("<INCP> Greeting {}".format(self.addr))
            self.socket.send(self.greeting)
            #Assumes default greeting
            #! Stop assuming default greeting
            resp = self.socket.recv(1)
            if resp == ACK:
                print("<INCP> {} acknowledged greeting".format(self.addr))
        else:
            msg = self.socket.recv(1)
            if msg == CHECK:
                print("<INCP> Check from {}".format(self.addr))
                self.socket.send(ACK)
                










            
