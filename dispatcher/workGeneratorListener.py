import sys
import socket
import os
import time
from connectionListener import *
from workGeneratorConnection import *

class WorkGeneratorListener(ConnectionListener):
	def __init__(self, port, addr):
		self.workComputerMap = {}
		self.nextInTurn = 0
		ConnectionListener.__init__(self, port, addr, "work generator")
		
	def accept(self, conn):
		print "Accepting work generator connection", conn
		return WorkGeneratorConnection(conn)

	def getJob(self):
		"""Get a job from a work generator"""
		n = len(self.connections)
		
		if self.nextInTurn >= n:
			self.nextInTurn = 0
		j = None
		if n > 0:	
			j = self.connections[self.nextInTurn].rx.getJob()
		self.nextInTurn+=1
		return j
		

		
