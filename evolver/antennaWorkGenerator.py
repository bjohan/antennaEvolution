import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import grid.workGeneratorClient
import grid.commandLine
import necInterface.antenna
import necInterface.band
from twisted.internet import stdio


band2m = necInterface.band.Band(144.0, 146.0, '2 Meter')


def myExit(args):
    print "Stopping reactor"
    client.stop()


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
    print "got result", result['work unit']['antenna id']

commands = {"quit": myExit}

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
