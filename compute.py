from necFileGenerator import *

class Compute:
	def __init__(self):
		self.antenna = None

	def setAntenna(self, antenna):
		self.antenna = antenna

	def addNecGeometry(self):
		print "Generating geometry for", self.antenna.name
		fg = NecFileGenerator('test.nec')
		fg.comment(self.antenna.name)
		fg = self.antenna.addNecGeometry(fg)
		fg.geometryEnd()
		fg.end()
		fg.frequency(10.0, 10.2, 21)
		fg.radiationPattern(0, 180, 20, 0, 360, 40)
		print str(fg)
		fg.write()
		#print "Adding gn_card for freespace"
		#ctx.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)
		
		#ctx.fr_card(0,2, 10.0e6, 0)
		#ctx.rp_card(2, 3, 2, 0, 5, 0, 0, 90.0, 90.0, 10.0, 10.0, 0.0, 0.0)


