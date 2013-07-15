class Element:
	def __init__(self, wireLength, straightLength, foldDirection, position):
		self.wireLength = wireLength
		self.straightLength = straightLength
		self.foldDirection = foldDirection
		self.position = position

	def __str__(self):
		s="Moxon element information:\n";
		s+="\t Length of wire: "+str(self.wireLength)	
		s+="\n\t Length of straight section"+str(self.straightLength)	
		s+="\n\t Folded in the "+self.foldDirection+" direction"	
		s+="\n\t position on boom: "+str(self.position)
		return s	
