import threading 
import Queue
import time

class ToComputerTransactor(threading.Thread):
	def __init__(self, sources, sinks):
		self.sources = sources
		self.sinks = sinks
		self.do = True
		threading.Thread.__init__(self)
		self.start()

	def run(self):
		mi = 0
		while self.do:
			j = self.sources.getJob()
			if j != None:
				print "Transacting job"
				self.sinks.sendJob()
			time.sleep(0.1)

	def stop(self):
		self.do = False
		
