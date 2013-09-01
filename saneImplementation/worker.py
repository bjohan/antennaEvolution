from workerConnection import *
from commandLine import *

def getWork():
	wu = wc.getWork()
	print wu.toString()

def shutDown():
	print "Shutting down"
	wc.stop()
	quit()

def compute():
	print "returning work"
	work = wc.rx.rxq.get_nowait()
	if work != None:
		wc.tx.txq.put(work)
		print "Work returned"
	else:
		print "no work received"

commands = { 	'gw': getWork,
		'quit': shutDown,
		'compute': compute}
cmd = CommandLine(commands)
wc = WorkerConnection('127.0.0.1')
cmd.mainLoop()
