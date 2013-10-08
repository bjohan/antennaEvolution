from twisted.internet import stdio
from twisted.protocols import basic
class CommandLine(basic.LineReceiver):
	from os import linesep as delimiter
	def __init__(self, cmdDict, tok = '> '):
		self.cmds = cmdDict
		self.tok = tok
		
	def prompt(self):
		self.transport.write(self.tok)

	def connectionMade(self):
		self.transport.write("Commandline started")
		self.prompt()

	def lineReceived(self, line):
		self.sendLine("Got data:"+line)
		args = line.split()
		if args[0] in self.cmds:
			if len(args) > 1:
				self.cmds[args[0]](args)
			else:
				self.cmds[args[0]]([])
		else:
			self.transport.write("Command not found\n")
		self.prompt()

		
