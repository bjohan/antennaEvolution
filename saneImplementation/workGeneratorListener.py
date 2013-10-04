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

	def registerWu(self, wuData, connId):
		print "WU data:", wuData
		wu = WorkUnit.fromString(wuData)
		wuNewId = self.currentWorkUnitId
		self.currentWorkUnitId += 1
		self.idMap[wuNewId] = (wu.seqNum, connId)
		print "idMap updated", self.idMap
		wu.seqNum = wuNewId
		return Message(1, wu.toString())

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
				return self.registerWu(data.data, self.connections[i].id)
			except Queue.Empty, e:
				pass
				
		return None

	def getConnection(self, connId):
		for c in self.connections:
			print "c.id", c.id
			if c.id == connId:
				return c
		else:
			print "No such connection", connId

	def put(self, msgIn):
		wu = WorkUnit.fromString(msgIn.data)
		print "reading from idMap", self.idMap
		print "looking for key", wu.seqNum
		(seqNum, connId) = self.idMap[wu.seqNum]
		wu.seqNum = seqNum
		msg = Message(1, wu.toString())
		c = self.getConnection(connId)
		#print dir(msg)
		#print "="*10
		#print dir(msg.data)
		print "Putting result in queue", msg
		c.tx.sendMessage(msg)
