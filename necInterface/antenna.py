import individual
import element
import analyzer
import drivenElement
import copy
import random
import necFileGenerator


class Antenna(individual.Individual):
    antennaNumber = 0

    def __init__(self):
        self.antennaId = Antenna.antennaNumber
        Antenna.antennaNumber += 1
        self.maxElements = 5
        self.elements = []
        self.name = "Default antenna name"
        self.bands = []
        self.fom = -1

    def generateNecCode(self, band, steps):
        fg = necFileGenerator.NecFileGenerator(None)
        fg.comment(self.name)
        fg = self.addNecGeometry(fg)
        fg.geometryEnd()
        fg.end()
        fg.frequency(band.start, band.stop, steps)
        fg.radiationPattern(-180, 180, 101, 0, 180, 101)
        return str(fg)

    def randomInit(self):
        numElements = int(1 + round(random.random() * (self.maxElements - 1)))
        self.elements = []
        for i in range(numElements):
            self.addElement(element.Element())
        self.checkDrivenElement()

    def addBands(self, bands):
        self.bands += bands

    def addElement(self, element):
        self.elements.append(element)

    def addElements(self, elements):
        self.elements += elements

    def setElements(self, elements):
        self.elements = []
        self.addElements(elements)

    def addNecGeometry(self, fg):
        for element in self.elements:
            fg = element.addNecGeometry(fg)
        return fg

    def evaluate(self, computer):
        if self.fom == -1:
            computer.setAntenna(self)
            result = computer.compute(5)
            a = analyzer.Analyzer(result)
            self.fom = a.getFigureOfMerit()
            print "Figure of merit", self.fom

    def __lt__(self, other):
        #print self.fom, "<", other.fom, "=",
        #if self.fom < other.fom:
        #   print "True"
        #else:
        #   print "False"
        return self.fom < other.fom

    def mutate(self):
        offs = copy.deepcopy(self)
        offs.fom = -1
        operation = round(random.random() * 3)
        if operation == 1:  # add
            if len(offs.elements) >= self.maxElements:
                operation = 2
            else:
                offs.addElement(element.Element())
        if operation == 2:  # del
            if len(offs.elements) <= 1:
                operation = 3
            else:
                e = round(random.random() * (len(offs.elements) - 1))
                print "deleting", e, "of", len(self.elements)
                del self.elements[int(e)]
        if operation == 3:  # modify
            e = int(round(random.random() * (len(offs.elements) - 1)))
            print "mutating", e, "of", len(offs.elements)
            offs.elements[int(e)].mutate()
        offs.checkDrivenElement()
        return offs

    def mate(self, partner):
        offspring = Antenna()
        nElements = 1 + round(random.random() * (self.maxElements - 1))
        elementPool = self.elements + partner.elements
        if nElements > len(elementPool):
            nElements = len(elementPool)
        usedElements = []
        while len(offspring.elements) < nElements:
            #pick new element
            while True:
                e = random.choice(range(len(elementPool)))
                if e not in usedElements:
                    break
            el = copy.deepcopy(elementPool[e])
            offspring.addElement(el)
        offspring.checkDrivenElement()
        return offspring

    def checkDrivenElement(self):
        if len(self.elements) == 0:
            print "WARNING, antenna has 0 elements"
        nDriven = 0
        n = 0
        for e in self.elements:
            if type(e) == drivenElement.DrivenElement:
                if nDriven >= 1:
                    print "Too many driven, making passive"
                    self.elements[n] = drivenElement.makePassive(
                        self.elements[n])
                nDriven += 1
            n += 1
        if nDriven == 0:
            n = random.choice(range(len(self.elements)))
            self.elements[n] = drivenElement.makeDriven(self.elements[n])

    def __str__(self):
        s = 'Antenna structure: \n'
        for e in self.elements:
            s += str(e)
        return s
