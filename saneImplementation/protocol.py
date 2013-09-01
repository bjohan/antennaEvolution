import struct
import threading

class Message:
	def __init__(self, type, data):
		self.data = data
		self.type = type

	def __str__(self):
		return "Message is of type %d and length %d"%(
			self.type, len(self.data))

class Encoder:
	
	def __init__(self):
		self.dataToSend = ''
		self.lock = threading.Lock()

	def appendMessage(self, msg):
		self.lock.acquire()
		l = len(msg.data)
		self.dataToSend+=struct.pack('LL',l, msg.type)
		self.dataToSend+=msg.data
		self.lock.release()

	def getDataToSend(self):
		self.lock.acquire()
		d = self.dataToSend
		self.dataToSend = ''
		self.lock.release()
		return d

class Decoder:
	def __init__(self):
		self.lock = threading.Lock()
		self.rxData = ''

	def appendReceivedData(self, data):
		self.lock.acquire()
		self.rxData+=data
		self.lock.release()

	def getMessage(self):
		self.lock.acquire()
		msg = None
		if len(self.rxData) >= 8:
			(l, t) = struct.unpack('LL', self.rxData[0:8])
			msgEnd = 8+l
			if len(self.rxData)>=msgEnd:
				data = self.rxData[8:msgEnd]
				self.rxData = self.rxData[msgEnd:]
				msg = Message(t, data)
		self.lock.release()
		return msg
				
			