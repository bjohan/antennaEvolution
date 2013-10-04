from workGeneratorServer import *
from computeServer import *
from commandLine import *

from twisted.internet import protocol
from twisted.application import service, internet

from twisted.internet import reactor
import twisted.internet
from twisted.internet import stdio, reactor

#Commandline callbacks
def myExit(args):
	print "Stopping reactor"
	reactor.stop()

commands = {"quit": myExit}


class ServerManagementFactory(protocol.ServerFactory):
	def __init__(self):
		self.connectionNumber = 0
		self.destinationFactory = None

	def getNewConnectionNumber(self):
		n = self.connectionNumber
		self.connectionNumber += 1
		return n

	def setDestinationFactory(self, factory):
		self.destinationFactory = factory

#Work generator server
workGeneratorFactory = ServerManagementFactory()
workGeneratorFactory.protocol = WorkGeneratorServer
workGeneratorFactory.clients = []

#Computer server
computeFactory = ServerManagementFactory()
computeFactory.protocol = ComputeServer
computeFactory.clients = []

#Received work units should be sent to the compute factory
workGeneratorFactory.setComputeClientFactory(computeFactory)

#Received results should be sent bac to the work generator factory
computeFactory.setWorkGeneratorFactory(workGeneratorFactory)

print "computeFactory", computeFactory
print "workGeneratorFactory", workGeneratorFactory

def main():
	reactor.listenTCP(0xbeef, computeFactory)
	reactor.listenTCP(0xdead, workGeneratorFactory)
	stdio.StandardIO(CommandLine(commands))
	reactor.run()

if __name__ == '__main__':
	main()
