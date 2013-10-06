from twisted.protocols import basic
from twisted.internet import protocol
import pickle


class ComputeServer(basic.LineReceiver):

    def connectionMade(self):
        self.workUnitsAtClient = 0
        self.computerId = self.factory.getNewConnectionNumber()
        print "new computer connected", self.computerId
        self.factory.clients.append(self)
        self.factory.workUnitManager.newComputer(self)

    def connectionLost(self, reason):
        print "lost computer"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        message = pickle.loads(line)
        if 'result' in message:
            self.returnResult(message)
            #message['number of clients'] = len(self.factory.clients)
            #self.factory.workGeneratorFactory.postResult(message)
        else:
            print "got something from compute client which is not a result:"
            print message

    def message(self, message):
        self.sendLine(pickle.dumps(message))

    def returnResult(self, result):
        self.factory.workUnitManager.postResult(result)
        self.workUnitsAtClient -= 1
        try:
            wu = self.factory.workUnitManager.getWorkUnitFromBuffer()
            self.sendWorkUnit(wu)
        except Exception, e:
            print "Exception while getting new work unit:", e

    def sendWorkUnit(self, wu):
        print "Sending work unit", wu
        self.workUnitsAtClient += 1
        self.message(wu)


class ComputeServerFactory(protocol.ServerFactory):
    def __init__(self):
        self.connectionNumber = 0
        self.workGeneratorFactory = None
        self.computer = -1
        self.workUnitManager = None

    def setWorkUnitManager(self, wum):
        self.workUnitManager = wum

    def getNewConnectionNumber(self):
        n = self.connectionNumber
        self.connectionNumber += 1
        return n

    def setWorkGeneratorFactory(self, factory):
        self.workGeneratorFactory = factory

    def postWorkUnit(self, wu):
        nClients = len(self.clients)
        if nClients > 0:
            self.computer = (self.computer + 1) % nClients
            self.clients[self.computer].sendWorkUnit(wu)
        else:
            print "No clients available. TODO implement buffering"
