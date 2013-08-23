import sys
import socket
import os
sys.path.append(os.path.abspath('../protocol'))
from communicatorThread import *

class EvolverConnection(CommunicatorThread):
	def __init__(self, serverAddr):
		print "Connecting to", serverAddr
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((serverAddr, 0xDEAD))
		CommunicatorThread.__init__(self, sock)
		print "Sending message"
		self.sendMessage('Hello from evolver')

	def processMessage(self, msg):
		print "TODO, process message for evolver client"
		print "Got message:", msg
		
