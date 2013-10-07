from simulationResult import *


class NecFileParser:
	def __init__(self, fileName=None):
		self.simulationResult = SimulationResult()
		f = open(fileName)
		self.data = f.read()
		self.parse()
	
	def parse(self):
		#print "Data is", len(self.data), "bytes"
		self.splitFrequencies()
		for frequency in self.frequencyData:
			self.simulationResult.addFrequency(self.parseFrequency(frequency))

	def parseFrequency(self, frqDat):
		fr = FrequencyResult()
		fr.setFrequency(self.getFrequency(frqDat))
		fr.setImpedance(self.getAntennaImpedance(frqDat))
		#currents = self.getAntennaCurrents(frqDat)
		#powerBudget = self.getPowerBudget(frqDat)
		fr.setRadiationPattern(self.getRadiationPattern(frqDat))
		return fr

	def getFrequency(self, dat):
		for line in dat.splitlines():
			if "FREQUENCY : " in line:
				return float(line.split()[2])

	def getAntennaImpedance(self, dat):
		section = self.getSection(dat, "ANTENNA INPUT PARAMETERS")
		lines = section.splitlines()
		for i in range(len(lines)):
			if "IMAGINARY" in lines[i]:
				break
		else:
			return
		values = lines[i+1].split();
		valDict = {}
		valDict['voltage real'] = float(values[2])
		valDict['voltage imaginary'] = float(values[3])
		valDict['current real'] = float(values[4])
		valDict['current imaginary'] = float(values[5])
		valDict['impedance real'] = float(values[6])
		valDict['impedance imaginary'] = float(values[7])
		valDict['admittance real'] = float(values[8])
		valDict['admittance imaginary'] = float(values[9])
		valDict['power'] = float(values[10])
		return valDict
	
	def getRadiationPattern(self, dat):
		section = self.getSection(dat, "RADIATION PATTERNS")
		lines = section.splitlines()
		for i in range(len(lines)):
			if "VOLTS/M" in lines[i]:
				break
		else:
			return
		parsedData = []
		for i in range(i+1, len(lines)):
			tokens = lines[i].split()
			if len(tokens) == 12:
				d = {}
				d['elevation'] = float(tokens[0])-90.0
				d['azimuth'] = float(tokens[1])
				d['major db'] = float(tokens[2])
				d['minor db'] = float(tokens[3])
				d['total db'] = float(tokens[4])
				d['axial ratio'] = float(tokens[5])
				d['tilt degrees'] = float(tokens[6])
				d['sense'] = tokens[7]
				d['e azimuth magnitude volts/m'] = float(tokens[8])
				d['e azimuth phase degrees'] = float(tokens[9])
				d['e elevation magnitude volts/m'] = float(tokens[10])
				d['e elevation phase degrees'] = float(tokens[11])
				parsedData.append(d)
		return parsedData	

	def splitFrequencies(self):
		token = "-------- FREQUENCY --------"
		last = self.data.find(token);
		#print "Skipping", last+len(token), "bytes at start"
		self.frequencyData = []
		dat = self.data[last+len(token):]	
		while True:
			nxt = dat.find(token)
			if nxt == -1:
				break
			self.frequencyData.append(dat[:nxt])
			dat = dat[nxt+len(token):]


	def getSection(self, data, section):
		preamble = '-'*7+' '
		sectionStart = preamble+section
		start = data.find(sectionStart)
		if start < 0:
			print "Unable to find section:", section
			return None
		post = start+len(sectionStart)*2
		last = data[post:].find(preamble)
		if last < 0:
			return data[start:]
			
		return data[start:post+last]
