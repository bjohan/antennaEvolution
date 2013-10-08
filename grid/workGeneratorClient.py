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
        #print "receive:", message
        if 'request work units' in message:
            units = message['request work units']
            for i in range(units):
                self.factory.sendWorkUnit()
        if 'result' in message:
            self.factory.evaluator(message)

    def disconnectWorkGeneratorClient(self):
        self.transport.loseConnection()

    def message(self, message):
        self.sendLine(pickle.dumps(message))


class WorkGeneratorClientFactory(ClientFactory):
    protocol = WorkGeneratorClientProtocol

    def __init__(self, generator, evaluator):
        self.clientConnection = None
        self.generator = generator
        self.evaluator = evaluator
        self.wuId = 0

    def sendWorkUnit(self):
        if self.clientConnection is not None:
            wu = self.generator()
            if wu is not None:
                workUnit = {'work unit': wu}
                workUnit['work unit id'] = self.wuId
                self.wuId += 1
                self.clientConnection.message(workUnit)
                print "Work unit sent"


class WorkGeneratorClient:
    def __init__(self, serverHostName, port, generator, evaluator):
        self.factory = WorkGeneratorClientFactory(generator, evaluator)
        reactor.connectTCP(serverHostName, port, self.factory)

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()
