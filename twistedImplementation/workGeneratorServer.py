"""The most basic chat protocol possible.

run me with twistd -y chatserver.py, and then connect with multiple
telnet clients to port 1025
"""

from twisted.protocols import basic
from dictUtils import *


class WorkGeneratorServer(basic.LineReceiver):
    def connectionMade(self):
	self.workGeneratorId = self.factory.getNewConnectionNumber()
        print "new work generator connected", self.workGeneratorId
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost work generator"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
	message = dictFromString(line)
        print "got:", message
        #for c in self.factory.clients:
        #    c.message(line)

    def message(self, message):
        #self.transport.write(message + '\n')
	self.sendLine(dictToString(message))

class WorkGeneratorServerFactory(protocol.ServerFactory):
	def __init__(self):
		self.connectionNumber = 0
		self.computeClientFactory = None

	def getNewConnectionNumber(self):
		n = self.connectionNumber
		self.connectionNumber += 1
		return n

	def setComputeClientFactory(self, factory):
		self.computeClientFactory = factory
	
	def postResult(self, result):
		print "TODO implement post result"
