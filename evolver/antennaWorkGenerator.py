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
import random

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
        #print "sending", job
        print len(initialPopulation), "left to initialize"
    else:
        while True:
            ps = len(population)
            mu = 0
            sigma = ps/3.0
            ca = int(round(min(abs(random.gauss(mu, sigma)),
                        len(population)-1)))
            cb = int(round(min(abs(random.gauss(mu, sigma)),
                            len(population)-1)))
            if ca != cb:
                break

        a = population[ca].mate(population[cb])
    job = {}
    job['nec code'] = a.generateNecCode(band2m, 21)
    job['antenna id'] = a.antennaId
    unevaluated.append({'job':job, 'ant':a})
    return job


def putInPopulation(result, fom):
    global population
    global unevaluated
    for i in unevaluated:
        if i['job']['antenna id'] == result['work unit']['antenna id']:
            unevaluated.remove(i)
            a = i['ant']
            a.fom = fom
            population.append(a)
            population = sorted(population)
            population.reverse()
            return
    else:
        print "Unknown antenna returned...."



def resultEvaluator(result):
    global nResults
    global population
    p = necInterface.necFileParser.NecFileParser(
        resultString = result['result'])
    sr = necInterface.simulationResult.SimulationResult()
    sr.append(p.simulationResult)
    a = necInterface.analyzer.Analyzer(sr)
    nResults += 1
    fom  = a.getFigureOfMerit()
    print "Fom:", fom
    putInPopulation(result, fom)
    if len(population) > populationSize:
        population=population[0:populationSize]

commands = {"quit": myExit, 'st': status}

#First initialize our population
populationSize = 200
initialPopulation = []
for i in range(populationSize):
    a = necInterface.antenna.Antenna()
    a.randomInit()
    initialPopulation.append(a)

population = []
unevaluated = []
#print initialPopulation[0].generateNecCode(band2m, 21)


client = grid.workGeneratorClient.WorkGeneratorClient('localhost', 0xdead,
                                                      workGenerator,
                                                      resultEvaluator)

stdio.StandardIO(grid.commandLine.CommandLine(commands))
client.run()
