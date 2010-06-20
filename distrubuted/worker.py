# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

import sys
import os

try:
    import poll
except ImportError:
    # This module is from a side-project, might not be in the
    # default python path:
    sys.path.append(os.path.join(os.path.dirname(__file__),"../pollbuster"))
    import poll

def voter( queue ):
    try:
        while True:
            job = queue.get()
            try:
                res = vote( job )
            except Exception, e:
                print >>sys.stderr, e # nice log plix
            finally:
                queue.task_done()
    except KeyboardInterrupt:
        pass

def vote( job ):
    tag = "%d]" % os.getpid()
    print tag, "voting on", job['url'], " (i=%d)"%job['i']
    from time import sleep
    sleep( 5 )
    print tag, "done"


# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

