import threading
import time
import socket
from computeConnection import *
from connectionListener import *

class ComputeClientListener(ConnectionListener):
	def __init__(self, port, addr):
		ConnectionListener.__init__(self, port, addr, "compute client")
		
	def accept(self, conn):
		print "Accepting work generator connection", conn
		return ComputeConnection(conn)

		
#class ComputeClientListener(threading.Thread):
#	def __init__(self, port, addr):
#		self.port = port
#		self.addr = addr
#		self.computers = []
#		self.continueRunning = True
#		threading.Thread.__init__(self)
#
#	def run(self):
#		print "Compute client listener thread started"
#		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		s.bind((self.addr, self.port))
#		s.listen(1)
#		s.setblocking(0)
#		print "Entering accept loop"
#		while self.continueRunning:
#			try:
#				conn, addr = s.accept()
#				print "incomming connection from", addr
#				#data = conn.recv(1024)
#				#print "Got data", data
#				self.computers.append(ComputeConnection(conn))
#				#conn.close()
#			except:
#				time.sleep(1)
#
#	def stop(self):
#		print "Stopping ComputeClientListener"
#		self.continueRunning = False
#		for c in self.computers:
#			c.stop()

