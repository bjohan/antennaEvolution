import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import grid.computeClient
import grid.commandLine
#from twisted.internet import reactor
from twisted.internet import stdio
import tempfile
client = None


def workFunction(workUnit):
    try:
        necFileName = tempfile.mktemp() + '.nec'
        resultFileName = tempfile.mktemp() + '.dat'
        necFile = open(necFileName, 'w')
        necFile.write(workUnit['nec code'])
        necFile.close()
        print "Starting nec simulation",
        os.system("nec2c -i " + necFileName + " -o " + resultFileName)
        print "Done"
        rf = open(resultFileName, 'r')
        result = rf.read()
        rf.close()
        os.remove(necFileName)
        os.remove(resultFileName)
    except Exception, e:
        print "Exception in work function", e
        result = None
    return result


def myExit(args):
    print "Stopping reactor"
    client.stop()
    #reactor.stop()


def status(args):
    print client

commands = {"quit": myExit, "st": status}
stdio.StandardIO(grid.commandLine.CommandLine(commands))


client = grid.computeClient.ComputeClient('localhost', 0xbeef, workFunction)
#The client.run() calls the reactor.run() so it does not return until it
# the reactor is stopped
client.run()
