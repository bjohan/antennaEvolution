import ast

def dictFromString(s):
	d=None
	try:
		d = ast.literal_eval(s)
	except:
		print "Error when converting", s
	return d

def dictToString(d):
	return d.__str__()
