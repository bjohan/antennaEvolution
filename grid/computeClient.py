from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import threading
import Queue
import pickle


class ComputeClientProtocol(LineReceiver):
    def connectionMade(self):
        self.factory.clientConnection = self
        self.message({'info': "Compute client"})

    def sendResult(self):
        self.message({'result': "Result from hard work"})

    def lineReceived(self, line):
        message = pickle.loads(line)
        #print "Got message:", message
        if message is not None:
            if 'work unit' in message:
                print "Got work unit, putting in worker queue"
                self.factory.workerThread.q.put(message)
                print self.factory.workerThread.q.qsize(), "jobs left"
        else:
            print "Message was None something is not what it should be..."

    def disconnectComputeClient(self):
        self.transport.loseConnection()

    def message(self, message):
        self.sendLine(pickle.dumps(message))


class ComputeClientFactory(ClientFactory):
    protocol = ComputeClientProtocol

    def __init__(self, workerThread):
        self.clientConnection = None
        self.workerThread = workerThread

    def postResult(self, result):
        if self.clientConnection is not None:
            self.clientConnection.message(result)


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
            print "Worker thread is waiting for a job"
            work = self.q.get()
            print "Got a job", self.q.qsize(), "jobs left"
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
        reactor.connectTCP('localhost', port, self.factory)

    def run(self):
        print "Starting reactor"
        reactor.run()

    def stop(self):
        reactor.stop()
        self.workerThread.q.put({'stop': 'now'})

    def __str__(self):
        a = "There are " + str(self.workerThread.q.qsize()) +\
            " work units in the queue"
        return a
