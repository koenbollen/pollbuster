# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

from google.appengine.ext import webapp

class IndexPage( webapp.RequestHandler ):
    def get(self ):
        try:
            fp = open( "pollbuster.tpl" )
            tpl = fp.read()
        except (IOError, OSError):
            tpl = "{content}"

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write( tpl )

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

