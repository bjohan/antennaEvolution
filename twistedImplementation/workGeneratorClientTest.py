import workGeneratorClient
import commandLine
import sys
from twisted.internet import stdio

nextJob = 0
if len(sys.argv) > 1:
    if sys.argv[1] == 'odd':
        nextJob = 1
    inc = 2
else:
    inc = 1

sentJobs = []
unexpectedJobs = []


def myExit(args):
    print "Stopping reactor"
    client.stop()


def workGenerator():
    global nextJob
    global sentJobs
    print "generating work"
    job = nextJob
    sentJobs.append(job)
    nextJob += inc
    if nextJob > 100001:
        while True:
            pass
    return "work " + str(job)


def resultEvaluator(result):
    global sentJobs
    global unexpectedJobs
    print "Evaluating result", result
    job = int(result['work unit'].split()[1])
    print "Got job:", job
    if job in sentJobs:
        sentJobs.remove(job)
    else:
        print "Got result for unexpected job"
        unexpectedJobs.append(job)

    print "there are", len(sentJobs), "pending results", sentJobs
    print len(unexpectedJobs), "unexpected results", unexpectedJobs

commands = {"quit": myExit}

client = workGeneratorClient.WorkGeneratorClient('localhost', 0xdead,
                                                 workGenerator,
                                                 resultEvaluator)

stdio.StandardIO(commandLine.CommandLine(commands))
client.run()
