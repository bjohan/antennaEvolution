import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import grid.workGeneratorClient
import grid.commandLine
#import necInterface.antenna
import necInterface.band
#import necInterface.necFileParser
#import necInterface.analyzer
#import necInterface.simulationResult
from twisted.internet import stdio
import time
import rollingPopulation

band2m = necInterface.band.Band(144.0, 146.0, '2 Meter')
tStart = time.time()
nResults = 0


def myExit(args):
    print "Stopping reactor"
    client.stop()


def status(args):
    global nResults
    print "Uptime", time.time() - tStart
    print "results", nResults
    print "frequency", nResults / (time.time() - tStart)


def populationStatus(args):
    print population


population = rollingPopulation.RollingPopulation(200, band2m, 0.04, 4, 21)

commands = {"quit": myExit, 'st': status, 'ps': populationStatus}

client = grid.workGeneratorClient.WorkGeneratorClient('localhost', 0xdead,
                                                      population.getNewIndividualAsJob,
                                                      population.handleResult)

stdio.StandardIO(grid.commandLine.CommandLine(commands))
client.run()
