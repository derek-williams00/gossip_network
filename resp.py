import argparse
import time

import incp


def openNode(t):
    print("<RESP> Opening responsive node for {}s".format(t))
    com = incp.IncpOverTcp()
    com.start()
    time.sleep(t)
    com.stop()


#initiate the parser
parser = argparse.ArgumentParser()


#add long and short argument
parser.add_argument("--time", "-t", help="set time (seconds) until close")


#read arguments from the command line
args = parser.parse_args()

#check for --address
if args.time != None:
    openNode(args.time)
else:
    openNode(60)
    
