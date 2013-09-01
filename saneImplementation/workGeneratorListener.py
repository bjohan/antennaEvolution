import sys
import socket
import os
import Queue
from connectionListener import *
from communicator import *
from workUnit import *
class WorkGeneratorListener(ConnectionListener):
	def __init__(self, addr, port):
		ConnectionListener.__init__(self, addr, port, "work generator")
		self.connToPoll = 0
		self.currentWorkUnitId = 0
		self.idMap = {}

	def accept(self, conn):
		print "Accepting work generator connection", conn
		return Communicator(conn)
		#return WorkGeneratorConnection(conn)

	def createAndRegisterWu(self, wuData, connId):
		print "WU data:", wuData
		wu = WorkUnit.fromString(wuData)
		wuNewId = self.currentWorkUnitId
		self.currentWorkUnitId += 1
		self.idMap[wuNewId] = (wu.seqNum, connId)
		wu.seqNum = wuNewId
		return wu

	def get(self):
		nConn = len(self.connections)
		if nConn == 0:
			return None
		self.connToPoll = self.connToPoll % nConn
		c = self.connToPoll
		for i in range(c, nConn)+range(c):
			try:
				data = self.connections[i].rx.rxq.get_nowait()
				self.connToPoll = i +1
				return self.createAndRegisterWu(data.data, i)
			except Queue.Empty, e:
				pass
				
		return None

	def getConnection(self, connId):
		for c in self.connections:
			if c.id == connId:
				return c
		else:
			print "No such connection", connId

	def put(self, data):
		wu = WorkUnit.fromString(data)
		(seqNum, connId) = self.idMap[wu.seqNum]
		wu.seqNum = seqNum
		c = self.getConnection(connId)
		c.tx.txq.put(wu.toString)
