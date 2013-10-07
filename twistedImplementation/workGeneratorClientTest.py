import workGeneratorClient
import commandLine
from twisted.internet import stdio


def myExit(args):
    print "Stopping reactor"
    client.stop()


def workGenerator():
    print "generating work"
    return "work"


def resultEvaluator(result):
    print "Evaluating result", result

commands = {"quit": myExit}

client = workGeneratorClient.WorkGeneratorClient('localhost', 0xdead,
                                                 workGenerator,
                                                 resultEvaluator)

stdio.StandardIO(commandLine.CommandLine(commands))
client.run()
