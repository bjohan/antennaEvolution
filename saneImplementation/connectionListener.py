import threading
import time
import socket

class ConnectionListener(threading.Thread):
	def __init__(self, addr, port, name, autoStart = True):
		self.port = port
		self.addr = addr
		self.connections = []
		self.continueRunning = True
		threading.Thread.__init__(self)
		self.name = name
		if autoStart:
			self.start()

	def run(self):
		print "Client listener thread:", self.name, "started"
		print "Listening for connections on", self.addr,":",self.port 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.addr, self.port))
		s.listen(1)
		s.setblocking(0)
		print "Entering accept loop"
		while self.continueRunning:
			try:
				conn, addr = s.accept()
				print "incomming connection from", addr
				print "Calling accept"
				self.connections.append(self.accept(conn))
				print "accept called"
				
				#conn.close()
			except Exception, e:
				#print "Exception while accepting connection", e
				time.sleep(1)
	def accept(self, connection):
		print "Unimplemented accept function, connection ignored for:", self.name
		return connection

	def stop(self):
		print "Stopping connection listener for:", self.name
		self.continueRunning = False
		for c in self.connections:
			c.stop()

