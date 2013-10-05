from twisted.internet import protocol
from twisted.protocols import basic
import dictUtils


class WorkGeneratorServer(basic.LineReceiver):
    def connectionMade(self):
        self.workGeneratorId = self.factory.getNewConnectionNumber()
        print "new work generator connected", self.workGeneratorId
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost work generator"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        message = dictUtils.dictFromString(line)
        print "got:", message
        if 'work unit' in message:
            print "Received message is a work unit"
            print "Augmenting work unit data with work generator id"
            message['generator id'] = str(self.workGeneratorId)
        self.factory.computeClientFactory.postWorkUnit(message)

    def message(self, message):
        self.sendLine(dictUtils.dictToString(message))


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
