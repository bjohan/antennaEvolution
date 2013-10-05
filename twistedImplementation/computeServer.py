from twisted.protocols import basic
from twisted.internet import protocol
import pickle
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
        message = pickle.loads(line)
        if 'result' in message:
            self.factory.workGeneratorFactory.postResult(message)
        else:
            print "got something from compute client which is not a result:"
            print message

    def message(self, message):
        self.sendLine(pickle.dumps(message))

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
            self.computer = (self.computer + 1) % nClients
            self.clients[self.computer].sendWorkUnit(wu)
        else:
            print "No clients available. TODO implement buffering"
