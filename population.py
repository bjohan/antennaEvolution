import random
import os
from necFileGenerator import *
class Population:
	def __init__(self, race = None, computer = None, size = 100, mutationRate = 0.05, 
			survivalRate = 0.8, initialPopulation = []):
		self.it = 0
		self.size = size
		self.mutationRate = mutationRate
		self.survivalRate = survivalRate
		self.race = race
		self.population = initialPopulation
		self.computer = computer
		numToSpawn = self.size-len(self.population)
		print "Creating initial population", numToSpawn, "individuals"
		for n in range(numToSpawn):
			ind = race()
			ind.randomInit()
			self.population.append(ind)

		print "Population size is now", len(self.population)

	def evaluate(self):
		print "Evaluating population"
		for i in self.population:
			i.evaluate(self.computer)
		print "Sorting population"
		self.sortPopulation()

	def sortPopulation(self):
		self.population = sorted(self.population)
		self.population.reverse()

	def killAllLosers(self):
		self.sortPopulation()
		numToKill = int(self.size*(1.0-self.survivalRate))
		print "Killing", numToKill, "individuals in population"
		self.population = self.population[0:-numToKill]
		

	def saveAntenna(self, antenna, filename):
		fg = NecFileGenerator('output/'+filename)
		fg.comment(antenna.name)
		fg = antenna.addNecGeometry(fg)
		fg.geometryEnd()
		fg.end()
		#fg.frequency(band.start, band.stop, steps)
		#fg.radiationPattern(-180, 180, 21, 0, 180, 21)
		#print "Writing NEC file"
		fg.write()
		self.computer.setAntenna(self)
		result = self.computer.compute(5)
		os.system('cp output/test.nec '+'output/sim'+filename)


	def populationCycle(self):
		self.evaluate()
		self.sortPopulation()
		self.saveAntenna(self.population[0], "gen"+str(self.it)+"best.nec")
		self.it += 1
		
		print "Foms for all antennas:", 
		for i in self.population:
			print i.fom,
		print ""
		self.killAllLosers()
		print "Foms for remaining antennas:", 
		for i in self.population:
			print i.fom,
		print ""
		numToMutate = int(self.size * self.mutationRate)
		numToBreed = int(self.size - len(self.population))-numToMutate
		self.generateMutants(numToMutate)
		self.swingersParty(numToBreed)

	def generateMutants(self, numToMutate):
		self.sortPopulation()
		for i in range(numToMutate):
			self.population.append(
					random.choice(self.population).mutate())
		

	def swingersParty(self, numToBreed):
		mu = 0
		sigma = len(self.population)/3.0;
		for i in range(numToBreed):
			while True:
				a = int(round(min(abs(random.gauss(mu, sigma)), 
						len(self.population)-1)))
				b = int(round(min(abs(random.gauss(mu, sigma)), 
						len(self.population)-1)))
				if a != b:
					break
			
			offspring = self.population[a].mate(self.population[b])

			self.population.append(offspring)
		
	def saveToFile(self, fn):
		f = open(fn, 'w')
		self.write(f)

	def write(self, fh):
		for i in self.population:
			i.write(fh)
		
