import socket
import sys
from computeClientListener import *
from workGeneratorListener import *
from toComputerTransactor import *
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
	ccl = ComputeClientListener(0xBEEF, listenAddress)
	wgl = WorkGeneratorListener(0xDEAD, listenAddress)
	ccl.start()
	wgl.start()
	tctx = ToComputerTransactor(wgl, ccl)	
	while True:
		cmd = raw_input('> ')
		print cmd
		if cmd == 'quit':
			ccl.stop()
			tctx.stop()
			wgl.stop()
			break
		if cmd == 'stat':
			print "Threre are", len(wgl.connections), " worker connections"
			for c in wgl.connections:
				print "Connection has", c.rx.rxq.qsize(), "jobs"
			
			print "Threre are", len(ccl.connections), " compute connections"
			for c in ccl.connections:
				print "Connection has", c.rx.rxq.qsize(), "results"
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.bind((listenAddress, 0xBEEF))
	#s.listen(1)
	#conn, addr = s.accept()
	#print "incomming connection from", addr
	#data = conn.recv(1024)
	#print "Got data", data

	#conn.close()

main()

