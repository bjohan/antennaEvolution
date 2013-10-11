import workGeneratorServer
import computeServer
import commandLine
import workUnitManager
#import sys
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet import stdio
#import twisted
import logo

#twisted.python.log.startLogging(sys.stderr)


def myExit(args):
    print "Stopping reactor"
    reactor.stop()


def requestWork(args):
    print "Sending work unit request"
    workGeneratorFactory.requestWorkUnit()


def checkBalance(args):
    print "checking balance"
    wuManager.checkBalance()


def status(args):
    print wuManager

commands = {"quit": myExit, "rw": requestWork, "cb": checkBalance,
            "st": status}


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


reactor.listenTCP(0xbeef, computeFactory)
reactor.listenTCP(0xdead, workGeneratorFactory)
stdio.StandardIO(commandLine.CommandLine(commands))
repeater = LoopingCall(wuManager.checkBalance)
repeater.start(10)
print logo.logo
reactor.run()
