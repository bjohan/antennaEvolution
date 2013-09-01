from commandLine import *
from workGeneratorListener import *
from workerListener import *
from mover import *
import time
def shutdown():
	wgl.stop()
	wl.stop()
	wum.stop()
	rum.stop()
	quit()

commands = { 'quit': shutdown}


cmd = CommandLine(commands)
wgl = WorkGeneratorListener('127.0.0.1', 0xDEAD)
wl = WorkerListener('127.0.0.1', 0xBEEF)
wum = Mover(wgl, wl, 'work generator ---wu---> worker')
rum = Mover(wl, wgl, 'work generator <---ru--- worker')
time.sleep(0.05)
cmd.mainLoop()
