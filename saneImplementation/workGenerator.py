from commandLine import *
from workeGeneratorConnection import *
from workUnit import *

def sendWork():
	wu = WorkUnit('Some work...')
	wgc.sendWorkUnit(wu)

def shutDown():
	print "Shutting down"
	wgc.stop()
	quit()

commands = {	'sw': sendWork , 
		'quit': shutDown}

cmd = CommandLine(commands)
wgc = WorkGeneratorConnection('127.0.0.1')
cmd.mainLoop()
