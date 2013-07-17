class NecFileParser:
	def __init__(self, fileName=None):
		f = open(fileName)
		self.data = f.read()
		self.parse()
	
	def parse(self):
		print "Data is", len(self.data), "bytes"
		self.splitFrequencies()

	def splitFrequencies(self):
		token = "-------- FREQUENCY --------"
		last = self.data.find(token);
		print "Skipping", last+len(token), "bytes at start"
		self.frequencyData = []
		dat = self.data[last+len(token):]	
		while True:
			nxt = dat.find(token)
			if nxt == -1:
				break
			self.frequencyData.append(dat[:nxt])
			dat = dat[nxt+len(token):]

		print "Found data for", len(self.frequencyData), "frequencies"
		for d in self.frequencyData:
			print "length", len(d)
		print self.frequencyData[0]
		print "Looking for power budget"
		dat = self.getSection(self.frequencyData[0], 'RADIATION')
		print dat

	def getSection(self, data, section):
		preamble = '-'*7+' '
		sectionStart = preamble+section
		start = data.find(sectionStart)
		if start < 0:
			print "Unable to find section:", section
			return None
		post = start+len(sectionStart)*2
		last = data[post:].find(preamble)
		print start, post, last
		if last < 0:
			return data[start:]
			
		return data[start:post+last]
