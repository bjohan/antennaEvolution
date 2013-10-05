from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import pickle


class WorkGeneratorClientProtocol(LineReceiver):
    def connectionMade(self):
        self.factory.clientConnection = self
        self.message({'info': "Work generator client"})

    def sendWork(self):
        self.message({'work unit': "A piece of hard work"})

    def lineReceived(self, line):
        message = pickle.loads(line)
        print "receive:", message

    def disconnectWorkGeneratorClient(self):
        self.transport.loseConnection()

    def message(self, message):
        self.sendLine(pickle.dumps(message))


class WorkGeneratorClientFactory(ClientFactory):
    protocol = WorkGeneratorClientProtocol

    def __init__(self):
        self.clientConnection = None


class WorkGeneratorClient:
    def __init__(self, serverHostName, port, generator, evaluator):
        self.factory = WorkGeneratorClientFactory()
        reactor.connectTCP(serverHostName, port, self.factory)

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()
