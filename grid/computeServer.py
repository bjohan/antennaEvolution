from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import protocol
import pickle


class ComputeServer(Int32StringReceiver):

    def connectionMade(self):
        ComputeServer.MAX_LENGTH = 10e7
        self.workUnitsAtClient = 0
        self.computerId = self.factory.getNewConnectionNumber()
        #print "new computer connected", self.computerId
        self.factory.clients.append(self)
        self.factory.workUnitManager.newComputer(self)

    #def lengthLimitSceeded(self, length):
    #    print "Length limit exceeded", length

    def connectionLost(self, reason):
        print "lost computer"
        self.factory.clients.remove(self)

    def stringReceived(self, line):
        message = pickle.loads(line)
        if 'result' in message:
            self.returnResult(message)
        #else:
        #    print "got something from compute client which is not a result:"
        #    print message

    def message(self, message):
        self.sendString(pickle.dumps(message))

    def returnResult(self, result):
        self.factory.workUnitManager.postResult(result)
        self.workUnitsAtClient -= 1
        try:
            self.factory.workUnitManager.requestWorkUnit()
            wu = self.factory.workUnitManager.getWorkUnitFromBuffer()
            if wu is None:
                print "Got none from buffer"
            else:
                self.sendWorkUnit(wu)

        except Exception, e:
            print "Exception while getting new work unit:", e

    def sendWorkUnit(self, wu):
        #print "Sending work unit", wu
        if wu is None:
            print 30 * '#"', "Got empty work unit"
        else:
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
