from twisted.internet import protocol
from twisted.protocols import basic
import pickle


class WorkGeneratorServer(basic.LineReceiver):
    def connectionMade(self):
        self.workGeneratorId = self.factory.getNewConnectionNumber()
        print "new work generator connected", self.workGeneratorId
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost work generator"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        message = pickle.loads(line)
        if 'work unit' in message:
            print "Received message is a work unit"
            print "Augmenting work unit data with work generator id"
            message['generator id'] = self.workGeneratorId
            self.factory.computeClientFactory.postWorkUnit(message)
        else:
            print "work generater sent something that is not a work unit:"
            print message

    def message(self, message):
        self.sendLine(pickle.dumps(message))


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
        print "Returning result to work generator who created work unit"
        if 'result' in result:
            generatorId = result['generator id']
            for client in self.clients:
                if client.workGeneratorId == generatorId:
                    print "Found client", generatorId, "sending result"
                    client.message(result)
        else:
            print result
            print "the above data does not contain a result"
        print "TODO implement post result"
