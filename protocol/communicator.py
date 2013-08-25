from sender import *
from receiver import *
class Communicator(threading.Thread):
	comId = 0
	def __init__(self, socket, autoStart = True):
		self.id = Communicator.comId
		Communicator.comId += 1
		socket.setblocking(0)
		socket.settimeout(0.1)
		self.rx = Receiver(socket)
		self.tx = Sender(socket)
		print "Communicator registered"

	def stop(self):
		print "Stopping communicator"
		self.rx.stop()
		self.tx.stop()
