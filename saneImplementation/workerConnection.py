import socket
from communicator import *
from workUnit import *
class WorkerConnection(Communicator):
	def __init__(self, serverAddr):
		print "Connecting to", serverAddr
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((serverAddr, 0xBEEF))
		Communicator.__init__(self, sock)

	def getWorkUnit(self, blocking = True):
		msg = self.rx.getMessage(blocking=blocking)
		if msg != None:
			return WorkUnit.fromString(msg)
		else:
			return None
		
