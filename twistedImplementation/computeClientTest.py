import computeClient
import commandLine
#from twisted.internet import reactor
from twisted.internet import stdio


client = None


def testWorkFunction(workUnit):
    print "Peforming work for", workUnit
    return "result"


def myExit(args):
    print "Stopping reactor"
    client.stop()
    #reactor.stop()


commands = {"quit": myExit}
stdio.StandardIO(commandLine.CommandLine(commands))


client = computeClient.ComputeClient('localhost', 0xbeef, testWorkFunction)
#The client.run() calls the reactor.run() so it does not return until it
# the reactor is stopped
client.run()
