import socket
import sys
from computeClientListener import *
from workGeneratorListener import *
def parseArguments():
	if len(sys.argv) != 2:
		printHelp()
	if sys.argv[1] == '-help':
		printHelp()
	return sys.argv[1]


def printHelp():
	print "Usge: python computeClinet.py listen_address"
	quit()



def main():
	listenAddress = parseArguments()
	#ccl = ComputeClientListener(0xBEEF, listenAddress)
	wgl = WorkGeneratorListener(0xDEAD, listenAddress)
	#ccl.start()
	wgl.start()
	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':
			#ccl.stop()
			wgl.stop()
			break
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.bind((listenAddress, 0xBEEF))
	#s.listen(1)
	#conn, addr = s.accept()
	#print "incomming connection from", addr
	#data = conn.recv(1024)
	#print "Got data", data

	#conn.close()

main()

