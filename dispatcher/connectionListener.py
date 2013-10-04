import threading
import time
import socket
from computeConnection import *
class ConnectionListener(threading.Thread):
	def __init__(self, port, addr, name):
		self.port = port
		self.addr = addr
		self.connections = []
		self.continueRunning = True
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		print "Client listener thread:", self.name, "started" 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.addr, self.port))
		s.listen(1)
		s.setblocking(0)
		print "Entering accept loop"
		while self.continueRunning:
			try:
				conn, addr = s.accept()
				print "incomming connection from", addr
				#data = conn.recv(1024)
				#print "Got data", data
				
				#self.computers.append(ComputeConnection(conn))
				print "Calling accept"
				self.connections.append(self.accept(conn))
				print "accept called"
				
				#conn.close()
			except socket.error, e:
				#print "Exception while accepting connection", e
				time.sleep(1)
	def accept(self, connection):
		print "Unimplemented accept function, connection ignored for:", self.name
		return connection

	def stop(self):
		print "Stopping connection listener for:", self.name
		self.continueRunning = False
		n = 0
		for c in self.connections:
			print "Stopping connection",n
			n+=1
			c.stop()

