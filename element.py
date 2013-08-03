class Element:
	def __init__(self, wireLength, straightLength, foldDirection, position):
		self.wireLength = wireLength
		self.straightLength = straightLength
		self.foldDirection = foldDirection
		self.position = position
		self.radius = 0.025

	def __str__(self):
		s="Moxon element information:\n";
		s+="\t Length of wire: "+str(self.wireLength)	
		s+="\n\t Length of straight section"+str(self.straightLength)	
		s+="\n\t Folded in the "+self.foldDirection+" direction"	
		s+="\n\t position on boom: "+str(self.position)+"\n"
		return s

	def addNecGeometry(self, g):
		#First comptute some coordinates element is created in xy-plane
		#positive y is "north" direction
		#xlength = 0.5*self.straightLength
		#ylength = 0.5*(self.wireLength-self.straightLength)
		#print "Adding moxon element. half width",xlength,"fold",ylength
		#if self.foldDirection == 'south':
		#	ylength = -ylength
		
		#First add straight wire
		#g.wire(-xlength, self.position, 0, xlength, 
		#			self.position, 0, self.radius)
		#Add east fold
		#g.wire(-xlength, self.position, 0,
		#			-xlength, self.position+ylength, 0, self.radius)
		#Add west fold
		#g.wire(xlength, self.position, 0,
		#			xlength, self.position+ylength, 0, self.radius)
		#return g	
		#First comptute some coordinates element is created in xy-plane
		#positive y is "north" direction
		ylength = 0.5*self.straightLength
		xlength = 0.5*(self.wireLength-self.straightLength)
		print "Adding moxon element. half width",ylength,"fold",xlength
		if self.foldDirection == 'south':
			xlength = -xlength
		
		#First add straight wire
		g.wire(	self.position, -ylength, 0, 
			self.position, ylength, 0, self.radius)
		#Add east fold
		g.wire(	self.position, -ylength, 0,
			self.position+xlength, -ylength, 0, self.radius)
		#Add west fold
		g.wire(	self.position, ylength, 0,
			self.position+xlength, ylength,  0, self.radius)
		return g	
