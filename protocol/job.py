import struct

class Job:
	idCntr = 0
	def __init__(self, data, jobId = None):
		if jobId == None:
			self.id = Job.idCntr
			Job.idCntr+=1
		else:
			self.id = jobId

		self.jobData = data
		
	def toString(self):
		return 'job'+struct.pack('l', self.id)+self.jobData

def jobFromString(string):
	print "Hello?"
	pType = string[0:3]
	jobId = struct.unpack('l', string[3:11])
	data = string[7:]
	print "Decoded", pType, jobId
	if pType == 'job':
		return Job(data, jobId)
	return None
		

