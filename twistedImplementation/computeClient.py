from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import stdio
import commandLine
import dictUtils


class ComputeClient(LineReceiver):
    def connectionMade(self):
        self.factory.clientConnection = self
        self.message({'info': "Compute client"})

    def sendResult(self):
        self.message({'result': "Result from hard work"})

    def lineReceived(self, line):
        message = dictUtils.dictFromString(line)
        print "Got message:", message

    def disconnectComputeClient(self):
        self.transport.loseConnection()

    def message(self, message):
        self.sendLine(dictUtils.dictToString(message))


class ComputeClientFactory(ClientFactory):
    protocol = ComputeClient

    def __init__(self):
        self.clientConnection = None


def myExit(args):
    print "Stopping reactor"
    reactor.stop()


def sendResult(args):
    factory.clientConnection.sendResult()


commands = {
    "quit": myExit,
    "sr": sendResult}


factory = ComputeClientFactory()
reactor.connectTCP('localhost', 0xbeef, factory)
stdio.StandardIO(commandLine.CommandLine(commands))
reactor.run()
