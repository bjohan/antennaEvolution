class CommandLine:
	def __init__(self, cmdDict, tok = '> '):
		self.cmds = cmdDict
		self.tok = tok
		
	def executeLine(self, line):
		args = line.split()
		if args[0] in self.cmds:
			if len(args) > 1:
				self.cmds[args[0]](args)
			else:
				self.cmds[args[0]]()
		else:
			print "Command not found"

	def mainLoop(self):
		print "Entering command line main loop"
		while True:
			self.executeLine(raw_input(self.tok))
			
		
