from band import *
from element import *
from drivenElement import *
from antenna import *
from compute import *
#Evolve a multibad moxon antenna.

band40Meter = Band(7.0,7.2, '40 meter')
band30Meter = Band(10.1,10.15, '30 meter')
band20Meter = Band(14.0,14.350, '20 meter')
band17Meter = Band(18.068,18.168, '17 meter') 
band15Meter = Band(21.0,21.450, '15 meter')
band12Meter = Band(24.89, 24.99, '12 meter')
band10Meter = Band(28.0,29.7, '10 meter')
band6Meter = Band(50.0,52.0, '6 meter')
band2Meter = Band(144.0,146.0, '2 meter')
	

bands = [band40Meter, band30Meter, band20Meter, band17Meter, band15Meter,
	band12Meter, band10Meter, band6Meter, band2Meter]

for b in bands:
	print b
	

element1 = Element(3.0, 2.0, 'north', 0);
element2 = Element(3.0, 2.0, 'south', 0);
print element1
print element2

print "Adding elements to antenna"
ant = Antenna()
ant.addElement(element1)
ant.addElement(element2)

print ant

cpt = Compute()
cpt.setAntenna(ant)
cpt.getNecContextWithGeometry()
