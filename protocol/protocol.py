import struct
import threading


class Encoder:
	def __init__(self):
		self.dataToSend = ''
		self.lock = threading.Lock()

	def appendMessage(self, msg):
		self.lock.acquire()
		l = len(msg)
		self.dataToSend+=struct.pack('L',l)
		self.dataToSend+=msg
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
		#print "rxbufsize:", len(self.rxData)
		#for d in self.rxData:
		#	print "0x%02x"%(ord(d)),
		#print 
		msg = ''
		if len(self.rxData) >= 8:
			l = struct.unpack('L', self.rxData[0:8])[0]
			#print "Message is", l, "bytes"
			msgEnd = 8+l
			if len(self.rxData)>=msgEnd:
				msg = self.rxData[8:msgEnd]
				self.rxData = self.rxData[msgEnd:]
		self.lock.release()
		return ''.join(msg)
				
			
