import threading
import socket
import os
import sys
sys.path.append(os.path.abspath('../protocol'))
from protocol import *

class ConnectionThread(threading.Thread):
	def __init__(self, addr):
		self.continueRunning = True
		self.d = Decoder()
		self.e = Encoder()
		print "Connecting to", addr
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		status = self.s.connect((addr, 0xBEEF))
		self.s.setblocking(0)
		print "Connection status", status
		threading.Thread.__init__(self)
		self.start()
		self.jobs = []
		self.sendMessage('Hello from client')
				
		#self.s.send('Hello from compute client')

	def run(self):
		while self.continueRunning:
			try:
				data = self.s.recv(1024)
			except:
				data = []
			if len(data) > 0:
				self.d.appendReceivedData(data)
			msg = self.d.getMessage()
			self.processMessage(msg)


	def processMessage(self, msg):
		if len(msg) > 0:
			print "Got message:", msg
		if msg == 'how many jobs?':
			self.sendMessage('jobs: %d'%(len(self.jobs)))

	def stop(self):
		self.continueRunning = False


	def sendBackResult(self, result):
		pass

	def getJob(self):
		pass

	def sendMessage(self, data):
		print "Sending", data
		self.e.appendMessage(data)
		self.s.send(self.e.getDataToSend())
	
