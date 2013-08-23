import sys
import socket
import os
from connectionListener import *
from workGeneratorConnection import *

class WorkGeneratorListener(ConnectionListener):
	def __init__(self, port, addr):
		ConnectionListener.__init__(self, port, addr, "work generator")
		
	def accept(self, conn):
		print "Accepting work generator connection", conn
		return WorkGeneratorConnection(conn)

		
