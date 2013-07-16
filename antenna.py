class Antenna:
	def __init__(self):
		self.elements = [];
		self.name = "Default antenna name"

	def addElement(self, element):
		self.elements.append(element)

	def addElements(self, elements):
		self.elements+=elements

	def setElements(self, elements):
		self.elements=[]
		self.addElements(elements)

	def putElementsInContext(self, ctx, tagStart = 0):
		lastTag = tagStart
		for element in self.elements:
			(ctx, lastTag) = element.putInContext(ctx, lastTag)
		return ctx

	def __str__(self):
		s = 'Antenna structure: \n';
		for e in self.elements:
			s+=str(e)
		return s
