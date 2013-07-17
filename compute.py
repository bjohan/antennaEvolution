from necFileGenerator import *
from necFileParser import *
import os;

class Compute:
	def __init__(self):
		self.antenna = None

	def setAntenna(self, antenna):
		self.antenna = antenna

	def compute(self):
		print "Generating geometry for", self.antenna.name
		fg = NecFileGenerator('output/test.nec')
		fg.comment(self.antenna.name)
		fg = self.antenna.addNecGeometry(fg)
		fg.geometryEnd()
		fg.end()
		fg.frequency(10.0, 10.2, 11)
		fg.radiationPattern(0, 180, 10, 0, 360, 10)
		print "Writing NEC file"
		fg.write()
		print "Running NEC"
		os.system("nec2c -i output/test.nec -o output/test_output.dat")
		parser = NecFileParser("output/test_output.dat")

