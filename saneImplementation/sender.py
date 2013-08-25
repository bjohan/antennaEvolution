from protocol import *
import threading
import Queue 

class Sender(threading.Thread):
	def __init__(self, socket):
		self.s = socket
		self.e = Encoder()
		self.txq = Queue.Queue()
		self.do = True
		threading.Thread.__init__(self)
		self.start()

	def sendMessage(self, msg):
		self.txq.put(msg.toString())

	def run(self):
		while self.do:
			try:
				msg = self.txq.get(timeout = 0.2)
				self.e.appendMessage(msg)
				print "Sending message"
				self.s.send(self.e.getDataToSend())
			except Queue.Empty, e:
				pass
		print "Sender thread stopped"


	def stop(self):
		print "Stopping sender thread"
		self.do = False
