def Antenna:
	def __init__(self):
		self.elements = [];

	def addElement(self, element):
		self.elements.append(element)

	def addElements(self, elements):
		self.elements+=elements

	def setElements(self, elements)
		self.elements=[]
		self.addElements(elements)
