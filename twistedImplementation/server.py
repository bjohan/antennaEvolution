import workGeneratorServer
import computeServer
import commandLine
from twisted.internet import reactor
from twisted.internet import stdio


def myExit(args):
    print "Stopping reactor"
    reactor.stop()


commands = {"quit": myExit}

#Work generator server
workGeneratorFactory = workGeneratorServer.WorkGeneratorServerFactory()
workGeneratorFactory.protocol = workGeneratorServer.WorkGeneratorServer
workGeneratorFactory.clients = []

#Computer server
computeFactory = computeServer.ComputeServerFactory()
computeFactory.protocol = computeServer.ComputeServer
computeFactory.clients = []

#Received work units should be sent to the compute factory
workGeneratorFactory.setComputeClientFactory(computeFactory)

#Received results should be sent bac to the work generator factory
computeFactory.setWorkGeneratorFactory(workGeneratorFactory)

print "computeFactory", computeFactory
print "workGeneratorFactory", workGeneratorFactory

reactor.listenTCP(0xbeef, computeFactory)
reactor.listenTCP(0xdead, workGeneratorFactory)
stdio.StandardIO(commandLine.CommandLine(commands))
reactor.run()
