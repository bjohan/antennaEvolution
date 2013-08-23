from protocol import *

e = Encoder()

d = Decoder()

e.appendMessage('Ralf ar en gnu\n')
e.appendMessage('Ralf ar dum\n')
e.appendMessage('Ralf gillar sno\n')
e.appendMessage('Blingo ar en glad gnu\n')
e.appendMessage('Min katt gillar kaffe\n')

d.appendReceivedData(e.getDataToSend())

while True:
	data = d.getMessage()
	if len(data) == 0:
		break
	print data
	for da in data:
		print "0x%02x"%(ord(da)),
	print
