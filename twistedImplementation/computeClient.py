#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
from commandLine import *
from dictUtils import *


class ComputeClient(LineReceiver):
	end="Bye-bye!"
	def connectionMade(self):
		self.factory.clientConnection = self
		self.message({'info':"Compute client"})
	        #self.sendLine("Hello, world!\nborpborp")
        	#self.sendLine("What a fine day it is.")
	        #self.sendLine(self.end)

	def sendResult(self):
		self.message({'result':"Result from hard work"})
		self.sendLine("Result from hard work")

	def lineReceived(self, line):
		message = dictFromString(line)
		print "Got message:", message
        	#print "receive:", line
	
	def disconnectComputeClient(self):
		self.transport.loseConnection()

	def message(self, message):
		self.sendLine(dictToString(message))

class ComputeClientFactory(ClientFactory):
	protocol = ComputeClient
	def __init__(self):
		self.clientConnection = None

def myExit(args):
	print "Stopping reactor"
	reactor.stop()


def sendResult(args):
	factory.clientConnection.sendResult()
commands = {	"quit": myExit, 
		"sr": sendResult}


factory = ComputeClientFactory()
reactor.connectTCP('localhost', 0xbeef, factory)
stdio.StandardIO(CommandLine(commands))
reactor.run()
