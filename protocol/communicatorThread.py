import threading
from protocol import *
class CommunicatorThread(threading.Thread):
	def __init__(self, socket, autoStart = True):
		self.continueRunning = True
		self.socket = socket
		self.socket.setblocking(0)
		self.d = Decoder()
		self.e = Encoder()
		threading.Thread.__init__(self)
		print "Communicator thread initialized"
		if autoStart:
			print "Communicator thread started"
			self.start()

	def run(self):
		print "communicatorThread started"
		while self.continueRunning:
			try:
				data = self.socket.recv(1024)
				if len(data) > 0:
					print "Got:", data
					self.d.appendReceivedData(data)
				msg = self.d.getMessage()
				if len(msg) > 0:
					self.processMessage(msg)
			except:
				pass

	def sendMessage(self, data):
		self.e.appendMessage(data)
		self.socket.send(self.e.getDataToSend())

	def stop(self):
		self.continueRunning = False

	def processMessage(self, msg):
		print "WARNING, unimplemented message processor"
