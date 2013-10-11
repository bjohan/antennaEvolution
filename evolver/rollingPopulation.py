import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import necInterface.antenna
import necInterface.band
import necInterface.necFileParser
import necInterface.analyzer
import necInterface.simulationResult
import random
import tempfile


class RollingPopulation():
    def __init__(self, populationSize, band, mutationRate, maxChildren,
                 frequencySteps):
        self.populationSize = populationSize
        self.band = band
        self.mutationRate = mutationRate
        self.maxChildren = maxChildren
        self.population = []
        self.unevaluatedPopulation = []
        self.frequencySteps = frequencySteps

    def getNewIndividual(self):
        if len(self.population) < self.populationSize:
            a = necInterface.antenna.Antenna()
            a.randomInit()
            return a
        if random.random() < self.mutationRate:
            return random.choice(self.population).mutate()
        else:
            while True:
                ps = len(self.population)
                mu = 0
                sigma = ps / 3.0
                ca = int(round(min(abs(random.gauss(mu, sigma)), ps - 1)))
                cb = int(round(min(abs(random.gauss(mu, sigma)), ps - 1)))
                if ca != cb:
                    break
            return self.population[ca].mate(self.population[cb])

    def getNewIndividualAsJob(self):
        a = self.getNewIndividual()
        job = {'nec code': a.generateNecCode(self.band, self.frequencySteps),
               'antenna id': a.antennaId}
        self.unevaluatedPopulation.append({'job': job, 'ant': a})
        return job

    def showAntenna(self, antNum):
        if antNum >= len(self.population):
            print "No such antenna"
            return
        fn = tempfile.mktemp() + '.dat'
        fh = open(fn, 'w')
        fh.write(self.population[antNum].necResult)
        fh.close()
        os.spawnl(os.P_NOWAIT, '/usr/bin/xnecview ' + fn)


    def putResultInPopulation(self, result, fom):
        for i in self.unevaluatedPopulation:
            if i['job']['antenna id'] == result['work unit']['antenna id']:
                self.unevaluatedPopulation.remove(i)
                a = i['ant']
                a.fom = fom
                #a.necCode = result['job']['nec code']
                a.necResult = result['result']
                self.population.append(a)
                self.population = sorted(self.population)
                self.population.reverse()
                if len(self.population) > self.populationSize:
                    self.population = self.population[0:self.populationSize]
                return
        else:
            print "Unknown antenna returned...."

    def handleResult(self, result):
        p = necInterface.necFileParser.NecFileParser(resultString =
                                                     result['result'])
        sr = necInterface.simulationResult.SimulationResult()
        sr.append(p.simulationResult)
        a = necInterface.analyzer.Analyzer(sr)
        fom = a.getFigureOfMerit()
        #print "Fom:", fom
        self.putResultInPopulation(result, fom)

    def __str__(self):
        a = "Current opulation size is " + str(len(self.population)) + "\n"
        a += "Maximum population size is " + str(self.populationSize) + "\n"
        a += "Unevaluated individuals " + str(len(self.unevaluatedPopulation))
        a += "\n"
        n = min(len(self.population), 10)
        print "Top ten individuals:"
        for i in range(n):
            a += "\tFom " + str(self.population[i].fom) + "\n"
        return a

