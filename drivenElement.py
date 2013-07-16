from element import *

class drivenElement(Element):
	def __init__(self, *args, **kwargs):
		super(args, kwargs)

	def __str__(self):
		s="Moxon element information:\n";
		s+="\t Length of wire: "+str(self.wireLength)	
		s+="\n\t Length of straight section"+str(self.straightLength)	
		s+="\n\t Folded in the "+self.foldDirection+" direction"	
		s+="\n\t position on boom: "+str(self.position)+"\n"
		return s

	def putInContext(self, ctx, tagStart):
		geo = ctx.get_geometry()
		#First comptute some coordinates element is created in xy-plane
		#positive y is "north" direction
		xlength = 0.5*self.straightLength
		ylength = 0.5*(self.wireLength-self.straightLength)
		print "Adding moxon element. half width",xlength,"fold",ylength,
		print "first tag", tagStart
		if self.foldDirection == 'south':
			ylength = -ylength
		
		#First add straight wire
		geo.wire(tagStart, 36, -xlength, self.position, 0,
					xlength, self.position, 0, self.radius,
					1.0, 1.0)
		tagStart+=1
		#Add east fold
		geo.wire(tagStart, 36, -xlength, self.position, 0,
					-xlength, self.position+ylength, 0,
					self.radius, 1.0, 1.0)
		tagStart+=1
		#Add west fold
		geo.wire(tagStart, 36, xlength, self.position, 0,
					xlength, self.position+ylength, 0,
					self.radius, 1.0, 1.0)
		return (ctx, tagStart)	
		pass
