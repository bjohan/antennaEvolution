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

class SimulationResult:
	def __init__(self):
		self.frequencies = []

	def addFrequency(self, f):
		self.frequencies.append(f)

	def __str__(self):
		s= "Simulation result for "+str(len(self.frequencies))+" frequencies"
		return s
