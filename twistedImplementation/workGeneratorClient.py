from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import stdio
import commandLine
import pickle


class WorkGeneratorClient(LineReceiver):
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
    protocol = WorkGeneratorClient

    def __init__(self):
        self.clientConnection = None


def myExit(args):
    print "Stopping reactor"
    reactor.stop()


def sendWork(args):
    factory.clientConnection.sendWork()

commands = {
    "quit": myExit,
    "sw": sendWork}


factory = WorkGeneratorClientFactory()
reactor.connectTCP('localhost', 0xdead, factory)
stdio.StandardIO(commandLine.CommandLine(commands))
reactor.run()
