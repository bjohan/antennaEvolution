import sys
import socket
import os
import Queue
from protocol import *
from connectionListener import *
from communicator import *
class WorkerListener(ConnectionListener):
	def __init__(self, addr, port):
		ConnectionListener.__init__(self, addr, port, "worker")
		self.nextWorker = 0

	def accept(self, conn):
		print "Accepting work generator connection", conn
		return Communicator(conn)
		#return WorkGeneratorConnection(conn)

	def get(self):
		for c in self.connections:
			try:
				data  = c.rx.getMessage()
				return data
			except Queue.Empty, e:
				pass

	def getNextWorkerConnection(self):
		#quick and dirty round robin
		numWorkers = len(self.connections)
		print numWorkers, "registered workers"
		if numWorkers == 0:
			return None
		self.nextWorker += 1
		self.nextWorker = self.nextWorker % numWorkers
		if numWorkers > 0:
			print "Sending job to worker", self.nextWorker
			return self.connections[self.nextWorker]
		
	def put(self, msg):
		c = self.getNextWorkerConnection()
		if c != None:
			c.tx.txq.put(msg)
		else:
			print "No workers, work unit discarded FIXTHIS!"
		

		
