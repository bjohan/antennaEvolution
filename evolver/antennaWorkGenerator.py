import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import grid.workGeneratorClient
import grid.commandLine
import necInterface.antenna
import necInterface.band
import necInterface.necFileParser
import necInterface.analyzer
import necInterface.simulationResult
from twisted.internet import stdio
import time

band2m = necInterface.band.Band(144.0, 146.0, '2 Meter')
tStart = time.time()
nResults = 0

def myExit(args):
    print "Stopping reactor"
    client.stop()

def status(args):
    global nResults
    print "Uptime", time.time()-tStart
    print "results", nResults
    print "frequency", nResults/(time.time()-tStart)

def workGenerator():
    if len(initialPopulation) > 0:
        a = initialPopulation[0]
        initialPopulation.remove(a)
        population.append(a)
        job = {}
        job['nec code'] = a.generateNecCode(band2m, 21)
        job['antenna id'] = a.antennaId
        #print "sending", job
        print len(initialPopulation), "left to initialize"
        return job


def resultEvaluator(result):
    global nResults
    p = necInterface.necFileParser.NecFileParser(
        resultString = result['result'])
    sr = necInterface.simulationResult.SimulationResult()
    sr.append(p.simulationResult)
    a = necInterface.analyzer.Analyzer(sr)
    nResults += 1
    print "Figure of merit is:", a.getFigureOfMerit()

commands = {"quit": myExit, 'st': status}

#First initialize our population
populationSize = 10000
initialPopulation = []
for i in range(populationSize):
    a = necInterface.antenna.Antenna()
    a.randomInit()
    initialPopulation.append(a)
population = []

#print initialPopulation[0].generateNecCode(band2m, 21)


client = grid.workGeneratorClient.WorkGeneratorClient('localhost', 0xdead,
                                                      workGenerator,
                                                      resultEvaluator)

stdio.StandardIO(grid.commandLine.CommandLine(commands))
client.run()
