#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
from commandLine import *
from dictUtils import *
class WorkGeneratorClient(LineReceiver):
	end="Bye-bye!"
	def connectionMade(self):
		self.factory.clientConnection = self
		self.message({'info': "Work generator client"})
	        #self.sendLine("Hello, world!\nborpborp")
        	#self.sendLine("What a fine day it is.")
	        #self.sendLine(self.end)

	def sendWork(self):
		self.message({'work unit':"A piece of hard work"})

	def lineReceived(self, line):
		print "raw data", line
		message = stringToDict(line)
        	print "receive:", message
	
	def disconnectWorkGeneratorClient(self):
		self.transport.loseConnection()

	def message(self, message):
		self.sendLine(dictToString(message))

class WorkGeneratorClientFactory(ClientFactory):
	protocol = WorkGeneratorClient
	def __init__(self):
		self.clientConnection = None

def myExit(args):
	print "Stopping reactor"
	reactor.stop()


def sendWork(args):
	factory.clientConnection.sendWork()

commands = {	"quit": myExit, 
		"sw": sendWork}


factory = WorkGeneratorClientFactory()
reactor.connectTCP('localhost', 0xdead, factory)
stdio.StandardIO(CommandLine(commands))
reactor.run()
