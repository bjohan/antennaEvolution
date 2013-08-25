from protocol import *
import socket
import threading
import Queue
from job import *
class Receiver(threading.Thread):
	def __init__(self, socket):
		self.socket = socket
		self.rxq = Queue.Queue()
		self.do = True
		self.d = Decoder()
		threading.Thread.__init__(self)
		self.start()

	def run(self):
		print "Receiver thread started"
		while self.do:
			try:
				data = self.socket.recv(1024)
				if len(data) > 0:
					print "Got:", data
					self.d.appendReceivedData(data)
				msg = self.d.getMessage()
				if msg != None:
					self.rxq.put(msg)
					print "Message queue length", self.rxq.qsize()
			except socket.error, e:
				pass
		print "Receiver thread exited"

	def getMessage(self):
		try:
			return self.rxq.get_nowait()
		except Queue.Empty, e:
			return None

	def stop(self):
		self.do = False

		
