import argparse
import time

import incp


def checkAddr(addr):
    print("<CHKPR> Attempting to check peer with address {}".format(addr))
    com = incp.IncpOverTcp()
    com.start()
    com.call(args.address)
    time.sleep(10)
    com.stop()


#initiate the parser
parser = argparse.ArgumentParser()


#add long and short argument
parser.add_argument("--address", "-a", help="set address of peer")


#read arguments from the command line
args = parser.parse_args()


print("Address : {}".format(args.address))

#check for --address
if args.address != None:
    checkAddr(args.address)
    
