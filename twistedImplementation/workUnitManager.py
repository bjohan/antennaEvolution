import Queue


class WorkUnitManager:
    def __init__(self, workGeneratorFactory, computeFactory):
        self.generators = workGeneratorFactory
        self.computers = computeFactory
        self.generators.setWorkUnitManager(self)
        self.computers.setWorkUnitManager(self)
        self.unitsAtClient = 2
        self.unitsInBuffer = 10
        self.unitsInBufferPerClient = 1
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

    def postWorkUnit(self, workGeneratorId, workUnit):
        nComputers = len(self.computers.clients)
        if nComputers > 0:
            self.computerRR = (self.computerRR + 1) % nComputers
            self.computers.clients[self.computerRR].message(workUnit)
        else:
            self.bufferWorkUnit(workUnit)

    def postResult(self, result):
        self.generators.postResult(result)

    def numberOfNewUnitsNeeded(self):
        missing = 0
        for client in self.computers.clients:
            if client.workUnitsAtClient < self.unitsAtClient:
                missing += self.unitsAtClient - client.workUnitsAtClient
        shouldBe = (self.unitsInBuffer +
                    len(self.computers.clients) * self.unitsInBufferPerClient)
        qs = self.wuq.qsize()
        if qs < shouldBe:
            missing += qs - shouldBe
        return missing - self.requestedWorkUnits

    def requestNewWorkUnitsIfNeeded(self):
        #First see how many new work units we need to get
        nwu = self.numberOfNewUnitsNeeded()
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
