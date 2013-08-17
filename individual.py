class Individual:
	def __init__(self):
		pass


	def evaluate(self, computer):
		print "Unimplemented evaluation"
			
	def mate(self, partner):
		print "Unimplemented mating procedure"

	def mutate(self):
		print "Implemented mutation procedure"

	def write(self, fh):
		print "unimplemented write to file"

	def __lt__(self, other):
		##print "unimplemented less than"
		return False	
