class FrequencyResult:
	def __init__(self):
		self.frequency = None
		self.radiationPattern = None
		self.impedance = None

	def setFrequency(self, f):
		self.frequency = f

	def setRadiationPattern(self, p):
		self.radiationPattern = p

	def setImpedance(self, i):
		self.impedance = i

	def getAzimuthGrid(self):
		azimuths = []
		for p in self.radiationPattern:
			if p['azimuth'] not in azimuths:
				azimuths.append(p['azimuth'])
		azimuths.sort()
		return azimuths

	def getElevationGrid(self):
		elevations = []
		for p in self.radiationPattern:
			if p['elevation'] not in elevations:
				elevations.append(p['elevation'])
		elevations.sort()
		return elevations

	def getRadiationPatternPoint(self, azimuth, elevation):
		for p in self.radiationPattern:
			if p['elevation']==elevation and p['azimuth']==azimuth:
				return p
		else:
			print "No radiation point for azi:", azimuth, "ele:", elevation
	
	def getGridByKey(self, key):	
		eles = self.getElevationGrid()
		azis = self.getAzimuthGrid()
		grid = [];
		for ele in eles:
			aziLine = []
			for azi in azis:
				p = self.getRadiationPatternPoint(azi, ele)
				aziLine.append(p[key])
			grid.append(aziLine)
		return grid

	def getMajorDbGrid(self):
		return self.getGridByKey('major db')


	def getFrontalGain(self):
		return self.getRadiationPatternPoint(0.0,0.0)['major db']

	def getRadiatedPower(self):
		return self.impedance['power']
		
class SimulationResult:
	def __init__(self):
		self.frequencies = []

	def addFrequency(self, f):
		self.frequencies.append(f)

	def append(self, simulationResult):
		self.frequencies+=simulationResult.frequencies

	def __str__(self):
		s= "Simulation result for "+str(len(self.frequencies))+" frequencies"
		return s
