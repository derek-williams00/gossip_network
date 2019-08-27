
import json
import socket

from threading import Thread


PORT = 2019
MAX_CONS = 5
BUFFER_SIZE = 1

COMCODES = {
    "check": b'\x01',
    "farewell": b'\x00',
    "acknowledge": b'\x02'
}


class GcpOverTcp:
    def __init__(self):
        self.addrs = AddressBook()
        self.box = []

        #Create server socket
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, PORT))
        self.server.listen(MAX_CONS)

    def handle(self):
        self.trim_box()

        #Handle new messages
        client, addr = self.server.accept()
        self.addrs.handle(addr)
        new_message = MessageHandler(client, addr, self.addrs)
        self.box.append(new_message)

    def trim_box(self):
        #Clear box of completed communications
        new_box = []
        for handler in self.box:
            if not handler.complete:
                new_box.append(handler)
        self.box = new_box

    def send_msg(self, addr, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, PORT))
        sock.send(msg)
        self.box.append(Messagehandler(sock, addr, self.addrs))

    def check(self, addr):
        self.send_msg(addr, COMCODES["check"])
        print("Checking {}".format(addr))

    def farewell(self, addr):
        self.send_msg(addr, COMCODES["farewell"])
        print("Saying farewell to {}".format(addr))
    
    def find_peers(self):
        pass

    def close(self):
        self.trim_box()
        for addr in self.addrs.get_all_current():
            self.farewell(addr)
        self.addrs.update_file()


class MessageHandler(Thread):
    def __init__(self, clientsocket, addr, addrbook):
        Thread.__init__(self)
        self.socket = clientsocket
        self.addr = addr
        self.addrbook = addrbook
        self.complete = False

    def run(self):
        self.header_byte = client.recv(1)
        if self.header_byte == COMCODES["check"]:
            print("Check from {}".format(self.addr))
            client.send(COMCODES["acknowledge"])
        elif self.header_byte == COMCODES["acknowledge"]:
            print("{} acknowledges".format(self.addr))
            self.addrbook.maintain(self.addr)
        elif self.header_byte == COMCODES["farewell"]:
            print("{} says farewell".format(self.addr))
            self.addrbook.archive(self.addr)
        client.close()
        self.complete = True


class AddressBook():
    FILE = "addrs.json"
    
    def __init__(self):
        self.addrs = []
        self.archives = []

        #Load addresses from json file
        try:
            file = open(AddressBook.FILE)
            peers_json = json.load(file)
            addrs = peers_json["addrs"]
            for addr in addrs:
                self.add_peer(addr)
            file.close()
        except FileNotFoundError:
            file = open(AddressBook.FILE, "w")
            data = dict()
            data["addrs"] = []
            json.dump(data, file)
            file.close()

    def handle(self, addr):
        self.add(addr)

    def add(self, addr):
        if not (addr in self.addrs):
            self.addrs.append(addr)
            print("Address {} added".format(addr))

    def remove(self, addr):
        self.addrs.remove(addr)
        print("Address {} removed".format(addr))

    def archive(self, addr):
        self.remove(addr)
        self.archives.append(addr)
        print("Address {} archived".format(addr))

    #! Add timer for every addr and maintain resets it
    def maintain(self, addr):
        self.add(addr)
        if addr in self.archives:
            self.archives.remove(addr)

    #! Archive unresponsive peers
    def trim(self):
        pass

    #! Update json file with current addrs
    def update_file(self):
        pass

    def get_all_current(self):
        #? Should this return a copy? 
        return self.addrs
        
        

if __name__ == "__main__":
    pass
