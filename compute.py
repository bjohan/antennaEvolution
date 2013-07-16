from PyNEC import *

class Compute:
	def __init__(self):
		self.antenna = None

	def setAntenna(self, antenna):
		self.antenna = antenna

	def getNecContextWithGeometry(self):
		print "Generating geometry for", self.antenna.name
		ctx = nec_context();
		ctx = self.antenna.putElementsInContext(ctx);
		ctx.geometry_complete(0)
		print "Adding gn_card for freespace"
		ctx.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)
