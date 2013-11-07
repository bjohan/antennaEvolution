from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor
import threading
import Queue
import pickle
import logo
import time


class ComputeClientProtocol(Int32StringReceiver):
    def connectionMade(self):
        ComputeClientProtocol.MAX_LENGTH = 10e7
        self.factory.clientConnection = self
        self.message({'info': "Compute client"})

    def sendResult(self):
        self.message({'result': "Result from hard work"})

    def stringReceived(self, line):
        message = pickle.loads(line)
        #print "Got message:", message
        if message is not None:
            if 'work unit' in message:
                #print "Got work unit, putting in worker queue"
                self.factory.workerThread.q.put(message)
                #print self.factory.workerThread.q.qsize(), "jobs left"
        else:
            print "Message was None something is not what it should be..."

    def disconnectComputeClient(self):
        self.transport.loseConnection()

    def message(self, message):
        self.sendString(pickle.dumps(message))


class ComputeClientFactory(ClientFactory):
    protocol = ComputeClientProtocol

    def __init__(self, workerThread):
        self.startTime = time.time()
        self.completedWorkUnits = 0.0
        self.clientConnection = None
        self.workerThread = workerThread

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed", reason

    def postResult(self, result):
        if self.clientConnection is not None:
            self.completedWorkUnits += 1
            self.clientConnection.message(result)

    def __str__(self):
        totTime = time.time() - self.startTime
        f = self.completedWorkUnits / totTime
        a = "Client has been running for %d seconds " % (totTime)
        a += "%d work units completed" % (self.completedWorkUnits)
        a += "at %f Hz" % (f)
        return a


class WorkerThread(threading.Thread):
    def __init__(self, workFunction):
        self.q = Queue.Queue()
        self.workFunction = workFunction
        threading.Thread.__init__(self)
        self.start()
        self.factory = None

    def setFactory(self, factory):
        self.factory = factory

    def run(self):
        print "Worker thread is running"
        while True:
            #print "Worker thread is waiting for a job"
            work = self.q.get()
            #print "Got a job", self.q.qsize(), "jobs left"
            if 'stop' in work:
                print "Received stop instruction"
                break
            if 'work unit' in work:
                result = self.workFunction(work['work unit'])
                work['result'] = result
                if self.factory is not None:
                    reactor.callFromThread(self.factory.postResult, work)


class ComputeClient:
    def __init__(self, serverHostName, port, workFunction):
        self.workerThread = WorkerThread(workFunction)
        self.factory = ComputeClientFactory(self.workerThread)
        self.workerThread.setFactory(self.factory)
        print "Connecting to", serverHostName
        reactor.connectTCP(serverHostName, port, self.factory)

    def run(self):
        print logo.logo
        print "Starting reactor"
        reactor.run()

    def stop(self):
        reactor.stop()
        self.workerThread.q.put({'stop': 'now'})

    def __str__(self):
        a = "There are " + str(self.workerThread.q.qsize()) +\
            " work units in the queue"
        return a
