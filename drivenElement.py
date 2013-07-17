from element import *

class DrivenElement(Element):
	def __init__(self, wireLength, straightLength, foldDirection, position):
		Element.__init__(self,wireLength,straightLength, foldDirection, position)

	def addNecGeometry(self, g):
		Element.addNecGeometry(self, g);
		drivenTag = g.tag-3;
		g.excite(drivenTag)
		return g	
