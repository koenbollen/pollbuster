# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch, InvalidURLError, DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup
import poll

class ExtactAjax( webapp.RequestHandler ):
    def post(self ):
        url = self.request.get( "url" )
        self.response.headers['Content-Type'] = 'text/json'

        if not url:
            self.response.out.write( '{"status":"failed","errstr":"missing url"}\n' )
            return
        
        errstr = None
        try:
            res = fetch( url )
        except InvalidURLError, e:
            errstr = "invalid url"
        except DownloadError, e:
            errstr = "unable to download"
        except: 
            errstr = "unknown error"

        if errstr is not None:
            self.response.out.write( 
                    '{"status":"failed","errstr":"%s"}\n' % errstr
                )
            return

        soup = BeautifulSoup( res.content )
        extractor = poll.Extractor( soup )

        result = extractor.detect()
        if len(result) < 1:
            self.response.out.write( 
                    '{"status":"failed","errstr":"no poll found"}\n' 
                )
            return
        mypoll = result[0]
        
        json.dump( {'status':"ok",'data': repr(mypoll)}, self.response.out )


# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

