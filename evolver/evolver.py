import socket
import sys
from evolverConnection import *


def parseArguments():
	if len(sys.argv) != 2:
		printHelp()
	if sys.argv[1] == '-help':
		printHelp()
	return sys.argv[1]


def printHelp():
	print "Usge: python evolver.py address_to_dispatcher"
	quit()



def main():
	serverAddress = parseArguments()
	print "Connecting to", serverAddress
	ec = EvolverConnection(serverAddress)

	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#status = s.connect((serverAddress, 0xDEAD))
	#print "Connection status", status
	#s.send('Hello from compute evolver')
	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':
			ec.stop()
			break


main()
