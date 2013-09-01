import socket
from communicator import *

class WorkGeneratorConnection(Communicator):
	def __init__(self, serverAddr):
		print "Connecting to", serverAddr
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((serverAddr, 0xDEAD))
		Communicator.__init__(self, sock)

	def sendWorkUnit(self, wu):
		msgData = wu.toString()
		msg = Message(1, msgData)
		self.tx.sendMessage(msg)
