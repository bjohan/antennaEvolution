import sys
import socket
import os
import Queue
sys.path.append(os.path.abspath('../protocol'))
from communicatorThread import *

class WorkGeneratorConnection(CommunicatorThread):
	def __init__(self, socket):
		self.workQueue = Queue.Queue()
		self.resultQueue = Queue.Queue()
		CommunicatorThread.__init__(self, socket)
		
	def processMessage(self, msg):
		print "wgl got message:", msg

	def getWork(self):
		return self.workQueue.get()
		
