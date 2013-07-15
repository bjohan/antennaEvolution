from PyNEC import *

class Compute:
	def __init__(self):
		pass

	def setAntenna(self, antenna):
		self.antenna = antenna

	def getNecContextWithStructure(self):
		ctx = nec_context();
		ctx = self.antenna.putElementsInContext(ctx);
