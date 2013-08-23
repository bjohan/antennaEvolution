import socket
import sys
import os
sys.path.append(os.path.abspath('../protocol'))
from protocol import *
from connectionThread import *
def parseArguments():
	if len(sys.argv) != 2:
		printHelp()
	if sys.argv[1] == '-help':
		printHelp()
	return sys.argv[1]


def printHelp():
	print "Usge: python computeClinet.py address_to_server"
	quit()



def main():
#	serverAddress = parseArguments()
	ct = ConnectionThread(parseArguments())
	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':			
			ct.stop()
			break

#	print "Connecting to", serverAddress
#	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	status = s.connect((serverAddress, 0xBEEF))
#	print "Connection status", status
#	s.send('Hello from compute client')


main()
