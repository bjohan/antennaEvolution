import socket
import sys
from evolverConnection import *
import os
sys.path.append(os.path.abspath('../protocol'))
from job import *

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

	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':
			ec.stop()
			break
		if cmd == 'sj':
			ec.sendJob(Job('deeerp'))


main()
