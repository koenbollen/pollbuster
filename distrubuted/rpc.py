# Koen Bollen <meneer koenbollen nl>
# 2010 GPL


from DocXMLRPCServer import DocXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading

__all__ = ( "RPCHandler", "start" )

count = 0

class RPCHandler( object ):

    def __init__(self, scheduler ):
        self.scheduler = scheduler


    def submit(self, url, pollid, choice, count ):
        """
        Submit a job to the distrubuted voter.

        Arguments:
          url    -- The url where the poll exists.
          pollid -- The number of the poll on that page.
          choice -- The choice in the poll to vote on.
          count  -- The number of votes to make using proxies.

        Returns the job id or False if the queue is full.
        """
        return self.scheduler.job( (url, pollid, choice, count) )


    def status(self, jid ):
        """Get the status of a submitted job."""
        info = self.scheduler.getinfo( jid )
        if not info:
            return "notfound"
        return info['status']


    def getinfo(self, jid ):
        """Get an info dictionary of a submitted job."""
        info = self.scheduler.getinfo( jid )
        return info


    def maxproxies(self ):
        """Return the maximum number of proxies availible."""
        return -1


def start( address, scheduler, debug=False ):
    global count

    if debug:
        s = DocXMLRPCServer( address, allow_none=True )
        s.register_introspection_functions()
    else:
        s = SimpleXMLRPCServer( address, allow_none=True )
    handler = RPCHandler( scheduler )
    s.register_multicall_functions()
    s.register_instance( handler )
    s.thread = threading.Thread( name="RPC-%d"%count, target=s.serve_forever )
    count+=1
    s.thread.daemon = True
    s.thread.start()
    return s, s.thread, handler

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

