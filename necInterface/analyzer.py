import math
class Analyzer:
    def __init__(self, simulationResult):
        self.result = simulationResult

    def getRadiationPatternMax(self):#,  lst, key):
        maximums = []
        for f in self.result.frequencies:
            maximums.append(
                self.getMaxFromListDict(
                    f.radiationPattern, 'total db'))
        #print "list of maximums", maximums
        return maximums

    def getMaxFromListDict(self, listDict, key):
        ma = None
        ma = listDict[0][key]
        for ent in listDict:
            if ent[key] > ma:
                ma = ent[key]

        return ma
    def getFigureOfMerit(self):
        if self.result == None:
            return -1
        gainMax = None
        gainMin = None
        powerMax = None
        powerMin = None
        powerAvg = 0
        gainAvg = 0
        for f in self.result.frequencies:
            g = f.getFrontalGain()
            p = f.getRadiatedPower()
            if gainMax == None:
                gainMax = g
                gainMin = g
            if powerMax == None:
                powerMax = p
                powerMin = p
            if math.isnan(p):
                print "Power is nan"
            if math.isnan(g):
                print "Gain is nan"
            powerAvg+=p
            gainAvg+=g
            powerMax = max(powerMax, p)
            powerMin = min(powerMin, p)
            gainMax = max(gainMax, g)
            gainMin = min(gainMin, g)
        try:
            deltaGain = gainMax-gainMin
            deltaPower = powerMax-powerMin
            gainAvg /= float(len(self.result.frequencies))
            powerAvg /= float(len(self.result.frequencies))
            print "Power--> Avg:",powerAvg,"max:", powerMax, "min:", powerMin, "delta:", deltaPower
            print "Gain--> Avg:",gainAvg,"max:", gainMax, "min:", gainMin, "delta:", deltaGain
            fom = powerMax*gainMax/(1.0+abs(deltaPower*deltaGain))
            #print "Figure of merit:", fom
            return fom
        except Exception, e:
            print e
            return -666

    #All methods below return max, min and avg
    def getFrontalGain(self):
        pass
    def getFrontalGainElevationLobeWidth(self):
        pass
    def getFrontalGainAzimuthLobeWidth(self):
        pass
    def getFrontToBackRatio(self):
        pass
    def getVSWR(self):
        pass
    def getImpedance(self):
        pass


