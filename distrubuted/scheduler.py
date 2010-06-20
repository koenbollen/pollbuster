# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

import Queue as queue
import multiprocessing
import worker
from time import time

class Scheduler():

    def __init__(self, queue_size, pool_size ):

        self.nextjid = 0
        self.queue = queue.Queue( queue_size )
        self.voter = multiprocessing.JoinableQueue()

        self.jobs = {}

        self.pool = []
        for i in xrange(pool_size):
            p = multiprocessing.Process( target=worker.voter, args=(self.voter,) )
            p.daemon = True
            p.start()


    def start(self ):
        self.run()

    def run(self ):
        while True:
            try:
                jid = self.queue.get( True, 1 )
            except queue.Empty:
                continue

            # TODO: status=verifying, test one vote before the mass

            self.jobs[jid]['status'] = "voting"
            self.jobs[jid]['stime'] = time()
            info = self.jobs[jid]

            for i in xrange( info['count'] ):
                innerinfo = info.copy()
                innerinfo['i'] = i
                self.voter.put( innerinfo )

            self.voter.join()
            self.jobs[jid]['status'] = "finish"
            self.jobs[jid]['etime'] = time()
            self.queue.task_done()


    def job(self, job ):

        if self.queue.full():
            return False

        jid = self.nextjid
        info = dict( zip( ("url","pollid","choice","count"), job ) )
        info['jid'] = jid
        info['qtime'] = time()
        info['stime'] = None
        info['etime'] = None
        info['status'] = "queued"

        self.jobs[jid] = info
        self.queue.put( jid, False )

        self.nextjid += 1
        return jid

    def getinfo(self, jid ):
        return self.jobs.get(jid)

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

