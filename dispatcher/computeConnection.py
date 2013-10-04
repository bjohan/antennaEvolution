import threading
import sys
import os
sys.path.append(os.path.abspath('../protocol'))
print sys.path
from protocol import *
from communicator import *
class ComputeConnection(Communicator):
	def __init__(self, socket):
		Communicator.__init__(self, socket)

#class ComputeConnection(threading.Thread):
#	def __init__(self, conn):
#		self.conn = conn
#		self.e = Encoder()
#		self.d = Decoder()
#		self.continueRunning = True
#		threading.Thread.__init__(self)
#		print "Compute connection created"
#		self.start()
#
#	def run(self):
#		self.getJobs()
#		while self.continueRunning:
#			data = self.conn.recv(1024)
#			if len(data) > 0:
#				self.d.appendReceivedData(data)
#
#				msg = self.d.getMessage()
#				if len(msg) > 0:
#					self.processMessage(msg)
#	def processMessage(self, msg):
#		print "Got", msg
#					
#	def getJobs(self):
#		self.sendMessage('how many jobs?')
#
#	def stop(self):
#		self.continueRunning = False
#	
#	def sendMessage(self, data):
#		self.e.appendMessage(data)
#		self.conn.send(self.e.getDataToSend())	
