class Band:
	def __init__(self, start, stop, name):
		self.start = start
		self.stop = stop
		self.name = name

	def __str__(self):
		return "Band named "+self.name+" from "+str(self.start)+" to "+str(self.stop)
