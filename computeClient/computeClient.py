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
	cc = ComputeConnection(parseArguments())
	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':			
			cc.stop()
			break
		if cmd == 'do':
			job = cc.getJob()
			if job != '':
				cc.sendResult('completed'+job) 

main()
