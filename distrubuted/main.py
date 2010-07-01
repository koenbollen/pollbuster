#!/usr/bin/env python
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL
#

import logging
import scheduler
import rpc

class DistrubutedVoter( object ):

    debug = False

    def __init__(self, address, queue_size, pool_size ):
        self.address = address
        self.scheduler = scheduler.Scheduler( queue_size, pool_size )
        self.rpc_server = None

    def start(self ):
        self.rpc_server = rpc.start(self.address, self.scheduler, self.debug)
        logging.notice( "distrubuted scheduler started" )
        self.scheduler.start()

    def shutdown(self ):
        logging.notice( "shutting down..." )
        self.rpc_server[0].shutdown()
        logging.notice( "shutdown" )


def main(): # testing main...
    dist = DistrubutedVoter( ('', 7655), 10, 2 )
    dist.debug = True
    try:
        dist.start()
    except KeyboardInterrupt:
        dist.shutdown()

    #
    # Client in interactive python shell:
    #
    #  (in debug mode check that address with a browser)
    #
    # >>> s = xmlrpclib.ServerProxy( "http://localhost:7655", allow_none=True )
    # >>> s.submit( "http://mypoll.com/", 0, 2, 10 )
    # 0
    # >>> s.submit( "http://anotherpoll.com/", 0, 3, 15 )
    # 1
    # >>> s.getinfo( 0 )
    # SNIP SNIP
    # >>> s.status( 1 )
    # "queued"
    #


if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

