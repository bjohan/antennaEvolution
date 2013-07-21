class Analyzer:
	def __init__(self, simulationResult):
		self.result = simulationResult
	
	def getRadiationPatternMax(self):#,  lst, key):
		maximums = []
		for f in self.result.frequencies:
			maximums.append(
				self.getMaxFromListDict(
					f.radiationPattern, 'total db'))
		print maximums

	def getMaxFromListDict(self, listDict, key):
		ma = None
		ma = listDict[0][key]
		for ent in listDict:
			if ent[key] > ma:
				ma = ent[key]

		return ma 
			
			
