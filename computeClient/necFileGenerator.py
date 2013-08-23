class NecFileGenerator:
	def __init__(self, filename):
		self.fn = filename
		self.commentData = ''
		self.geometryData = ''
		self.exciteData = ''
		self.radiationData = ''
		self.frequencyData = ''
		self.endData = ''
		self.tag = 1
		
	def comment(self, comment):
		self.commentData+="CM "+comment+"\n"

	def wire(self, x1, y1, z1, x2, y2, z2, radius, segments = 35):
		t = self.tag
		self.tag+=1
		self.geometryData+="GW\t%d\t%d\t%e\t%e\t%e\t%e\t%e\t%e\t%e\n"%(
			t, segments, x1, y1, z1, x2, y2, z2, radius)


	def geometryEnd(self):
		self.geometryData+="GE\t%d\t%d\t%e\t%e\t%e\t%e\t%e\t%e\t%e\n"%(
			0, 0, 0, 0, 0, 0, 0, 0, 0)

	def end(self):
		self.endData+="EN\t%d\t%d\t%d\t%d\t%e\t%e\t%e\t%e\t%e\n"%(
			0, 0, 0, 0, 0, 0, 0, 0, 0)

	def excite(self, tag , segment = 18):
		self.exciteData+="EX\t%d\t%d\t%d\t%d\t%e\t%e\t%e\t%e\t%e\n"%(
		0, tag, segment, 0, 0, 0, 0, 0, 0)

	def frequency(self, start, stop, steps):
		delta = float(stop-start)/(steps-1)
		self.frequencyData+="FR\t%d\t%d\t%d\t%d\t%e\t%e\t%e\t%e\t%e\t%e\n"%(
			0, steps, 0, 0, start, delta, 0, 0, 0, 0)

	def radiationPattern(self, aziStart, aziStop, aziSteps, 
					eleStart, eleStop, eleSteps):
		deltaAzi = float(aziStop-aziStart)/(aziSteps-1)
		deltaEle = float(eleStop-eleStart)/(eleSteps-1)
		self.radiationData+="RP\t%d\t%d\t%d\t%d\t%e\t%e\t%e\t%e\t%e\t%e\n"%(
			0, eleSteps, aziSteps, 1400, eleStart, aziStart, deltaEle, deltaAzi,0.0,0.0)

	def __str__(self):
		s = self.commentData
		s+= "CE\n"
		s+=self.geometryData
		s+=self.exciteData
		s+=self.frequencyData
		s+=self.radiationData
		s+=self.endData
		return s
		
	def write(self):
		fh = open(self.fn,'w')
		s = list(str(self))
		for i in range(len(s)):
			if s[i] == '\t':
				s[i] = ' '
		s = ''.join(s)
		fh.write(s)
		fh.close()
