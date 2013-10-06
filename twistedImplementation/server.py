import workGeneratorServer
import computeServer
import commandLine
import workUnitManager
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet import stdio


def myExit(args):
    print "Stopping reactor"
    reactor.stop()


def requestWork(args):
    print "Sending work unit request"
    workGeneratorFactory.requestWorkUnit()

commands = {"quit": myExit, "rw": requestWork}


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

#create work unit manager
wuManager = workUnitManager.WorkUnitManager(workGeneratorFactory,
                                            computeFactory)


print "computeFactory", computeFactory
print "workGeneratorFactory", workGeneratorFactory

reactor.listenTCP(0xbeef, computeFactory)
reactor.listenTCP(0xdead, workGeneratorFactory)
stdio.StandardIO(commandLine.CommandLine(commands))
repeater = LoopingCall(wuManager.checkBalance)
repeater.start(1)
reactor.run()
