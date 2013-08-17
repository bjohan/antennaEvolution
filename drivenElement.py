from element import *

class DrivenElement(Element):
	def __init__(self, bendLength, straightLength, foldDirection, position):
		Element.__init__(self,bendLength,straightLength, foldDirection, position)

	def addNecGeometry(self, g):
		Element.addNecGeometry(self, g);
		drivenTag = g.tag-3;
		g.excite(drivenTag)
		return g


def makeDriven(e):
	return DrivenElement(e.bendLength, e.straightLength, e.foldDirection,
				e.position)	
