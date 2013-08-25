import struct
class WorkUnit:
	numUnits = 0
	def __init__(self, work = None, seqNum = None):
		if seqNum == None:
			self.seqNum = WorkUnit.numUnits
			WorkUnit.numUnits += 1
		else:
			self.seqNum = seqNum
		self.work = work
	
	def toString(self):
		return struct.pack("l", self.seqNum)+self.work

	@classmethod
	def fromString(cls,string):
		seqNum = struct.unpack("l", string[0:8])
		work = string[8:]
		return cls(work, seqNum)

	def __str__(self):
		s = "Work unit # "+str(self.seqNum)+"."
		if self.work != None:
			s+=" Work is "+len(self.work)+" bytes"
		else:
			s+="Has no work"

		return s
