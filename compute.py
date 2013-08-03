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
		fg.frequency(19.0, 20.0, 11)
		fg.radiationPattern(-180, 180, 21, 0, 180, 21)
		print "Writing NEC file"
		fg.write()
		print "Running NEC"
		os.system("nec2c -i output/test.nec -o output/test_output.dat")
		parser = NecFileParser("output/test_output.dat")
		return parser.simulationResult


