import Queue


class WorkUnitManager:
    def __init__(self, workGeneratorFactory, computeFactory):
        self.generators = workGeneratorFactory
        self.computers = computeFactory
        self.generators.setWorkUnitManager(self)
        self.computers.setWorkUnitManager(self)
        self.unitsAtClient = 2
        self.unitsInBuffer = 2
        self.unitsInBufferPerClient = 2
        self.generatorRR = -1
        self.computerRR = -1
        self.requestedWorkUnits = 0
        self.wuq = Queue.Queue()

    def requestWorkUnit(self):
        nGenerators = len(self.generators.clients)
        if nGenerators > 0:
            msg = {'request work units': 1}
            self.generatorRR = (self.generatorRR + 1) % nGenerators
            self.generators.clients[self.generatorRR].message(msg)
            self.requestedWorkUnits += 1

    #def postWorkUnit(self, workGeneratorId, workUnit):
    #    nComputers = len(self.computers.clients)
    #    if nComputers > 0:
    #        self.computerRR = (self.computerRR + 1) % nComputers
    #        self.computers.clients[self.computerRR].message(workUnit)
    #    else:
    #        self.bufferWorkUnit(workUnit)

    def postResult(self, result):
        self.generators.postResult(result)

    def numberOfNewUnitsNeeded(self):
        missing = 0
        for client in self.computers.clients:
            if client.workUnitsAtClient < self.unitsAtClient:
                print "client has", client.workUnitsAtClient, "work units"
                missing += self.unitsAtClient - client.workUnitsAtClient
        print missing, "work units missing for the clients"
        shouldBe = (self.unitsInBuffer +
                    len(self.computers.clients) * self.unitsInBufferPerClient)
        print "Desired number of work units for server buffer:", shouldBe
        qs = self.wuq.qsize()
        print "there are approx", qs, "work units in buffer"
        if qs < shouldBe:
            missing += shouldBe - qs

        print "a total of", missing, "work units are missing"
        print self.requestedWorkUnits, "have been requested"
        return missing - self.requestedWorkUnits

    def requestNewWorkUnitsIfNeeded(self):
        #First see how many new work units we need to get
        nwu = self.numberOfNewUnitsNeeded()
        print nwu, "work units needed"
        if nwu > 0:
            #get as many as needed
            for i in range(nwu):
                self.requestWorkUnit()

    def sendNewWorkUnitsToComputers(self):
        for c in self.computers.clients:
            if c.workUnitsAtClient < self.unitsAtClient:
                if not self.wuq.empty():
                    c.sendWorkUnit(self.wuq.get())
                else:
                    print "Out of work units"
                    return

    def checkBalance(self):
        self.requestNewWorkUnitsIfNeeded()
        self.sendNewWorkUnitsToComputers()

    def newComputer(self, computer):
        for i in range(self.unitsAtClient):
            self.requestWorkUnit()
            if not self.wuq.empty():
                computer.sendWorkUnit(self.wuq.get())
            else:
                print "Out of work units"
                return

    def getWorkUnitFromBuffer(self):
        if not self.wuq.empty():
            return self.wuq.get()
        else:
            print "Out of work units"

    def bufferWorkUnit(self, workUnit):
        self.requestedWorkUnits -= 1
        if workUnit is None:
            print "Got None Wu", 30 * "<>"
        print "BUFFERING", workUnit
        self.wuq.put(workUnit)

    def __str__(self):
        a = "WorkUnitManager has " + str(len(self.computers.clients))
        a += " computer clients and " + str(len(self.generators.clients))
        a += " generator clients.\n"
        a += "the current approximate buferd amount of work is: "
        a += str(self.wuq.qsize()) + " work units\n"
        for c in self.computers.clients:
            a += "\t client has " + str(c.workUnitsAtClient) + "work units\n"

        return a
