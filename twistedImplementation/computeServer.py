from twisted.protocols import basic
from twisted.internet import protocol
from dictUtils import *
computeNumber = 0
class ComputeServer(basic.LineReceiver):

    def connectionMade(self):
        self.computerId = self.factory.getNewConnectionNumber()
        print "new computer connected", self.computerId
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "lost computer"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        message = dictFromString(line)
        print "got message:", message
        #print "got result", repr(line)
            #for c in self.factory.clients:
        #   c.message(line)

    def message(self, message):
        #self.transport.write(message + '\n')
        self.sendLine(dictToString(message))

    def sendWorkUnit(self, wu):
        print "Sending work unit", wu
        self.message(wu)


class ComputeServerFactory(protocol.ServerFactory):
    def __init__(self):
        self.connectionNumber = 0
        self.workGeneratorFactory = None
        self.computer = -1

    def getNewConnectionNumber(self):
        n = self.connectionNumber
        self.connectionNumber += 1
        return n

    def setWorkGeneratorFactory(self, factory):
        self.workGeneratorFactory = factory

    def postWorkUnit(self, wu):
        nClients = len(self.clients)
        if nClients > 0:
            self.computer = (self.computer+1)%nClients
            self.clients[self.computer].sendWorkUnit(wu)
        else:
            print "No clients available. TODO implement buffering"

