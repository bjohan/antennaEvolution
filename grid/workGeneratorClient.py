from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor
import pickle
import logo

class WorkGeneratorClientProtocol(Int32StringReceiver):
    def connectionMade(self):
        WorkGeneratorClientProtocol.MAX_LENGTH = 10e7
        self.factory.clientConnection = self
        self.message({'info': "Work generator client"})

    def sendWork(self):
        self.message({'work unit': "A piece of hard work"})

    def stringReceived(self, line):
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
        self.sendString(pickle.dumps(message))


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
                #print "Work unit sent"


class WorkGeneratorClient:
    def __init__(self, serverHostName, port, generator, evaluator):
        self.factory = WorkGeneratorClientFactory(generator, evaluator)
        reactor.connectTCP(serverHostName, port, self.factory)

    def run(self):
        print logo.logo
        reactor.run()

    def stop(self):
        reactor.stop()
