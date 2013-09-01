import threading
import time
class Mover(threading.Thread):
	def __init__(self, source, sink, message):
		self.source = source
		self.sink = sink
		self.do = True
		threading.Thread.__init__(self)
		self.msg = message;
		self.start()

	def run(self):
		while self.do:
			d = self.source.get()
			if d != None:
				print "src", self.source, "dst", self.sink
				print self.msg
				self.sink.put(d)
			else:
				time.sleep(0.2)

	def stop(self):
		self.do = False
