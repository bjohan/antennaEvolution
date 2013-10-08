from twisted.internet import protocol
from twisted.protocols import basic
import pickle


class WorkGeneratorServer(basic.LineReceiver):
    def connectionMade(self):
        self.workGeneratorId = self.factory.getNewConnectionNumber()
        print "new work generator connected", self.workGeneratorId
        self.factory.clients.append(self)
        self.factory.workUnitManager.checkBalance()
        self.requestedWorkUnits = 0

    def connectionLost(self, reason):
        print "Lost work generator"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        message = pickle.loads(line)
        if 'work unit' in message:
            #print "Received message is a work unit"
            #print "Augmenting work unit data with work generator id"
            message['generator id'] = self.workGeneratorId
            #self.factory.computeClientFactory.postWorkUnit(message)
            self.factory.workUnitManager.bufferWorkUnit(message)
            self.requestedWorkUnits -= 1
        else:
            print "work generater sent something that is not a work unit:"
            print message

    def message(self, message):
        self.sendLine(pickle.dumps(message))

#    def requestWorkUnits(self, num):
#        self.message({'request work units': 1})


class WorkGeneratorServerFactory(protocol.ServerFactory):
    def __init__(self):
        self.connectionNumber = 1000
        self.computeClientFactory = None
        self.rrCounter = -1
        self.requestedWorkUnits = 0
        self.workUnitManager = None

    def setWorkUnitManager(self, wum):
        self.workUnitManager = wum

    def getNewConnectionNumber(self):
        n = self.connectionNumber
        self.connectionNumber += 1
        return n

    def setComputeClientFactory(self, factory):
        self.computeClientFactory = factory

#    def requestWorkUnit(self):
#        nClients = len(self.clients)
#        if nClients > 0:
#            self.rrCounter = (self.rrCounter + 1) % nClients
#            self.clients[self.rrCounter].requestWorkUnits(1)
#            self.requestedWorkUnits += 1

    def postResult(self, result):
        #print "Returning result to work generator who created work unit"
        if 'result' in result:
            generatorId = result['generator id']
            #print "Search start, there are:", len(self.clients), "generators"
            for client in self.clients:
                #print "gen id is", client.workGeneratorId, "?", generatorId
                if client.workGeneratorId == generatorId:
                    #print "Found client", generatorId
                    client.message(result)
                    break
            else:
                print "Work Generator", generatorId, "not found"
        else:
            print result
            print "the above data does not contain a result"
        #print "TODO implement post result"
