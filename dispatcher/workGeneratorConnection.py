import sys
import socket
import os
import Queue
sys.path.append(os.path.abspath('../protocol'))
from communicator import *
from job import *

class WorkGeneratorConnection(Communicator):
	def __init__(self, socket):
		Communicator.__init__(self, socket)
