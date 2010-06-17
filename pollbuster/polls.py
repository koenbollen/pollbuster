# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch, InvalidURLError, DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup
import poll

class FetchError( Exception ):
    pass

def poll2dict( pll ):
    d = dict(zip(('id', 'name', 'method', 'action', 'groupname', 'choices',
        'hiddens', 'specials'), pll))
    hiddens = []
    specials = []
    for h in d['hiddens']:
        hiddens.append( dict(zip(('name', 'value'), h)) )
    for s in d['specials']:
        s = dict(zip(('type','name','value','special'), s))
        specials.append( s )
    d['hiddens'] = hiddens
    d['specials'] = specials
    return d

class ExtactAjax( webapp.RequestHandler ):
    def post(self ):
        url = self.request.get( "url" )

        try:
            result = self.fetch( url )
        except FetchError, e:
            reply = {
                    'status': "error",
                    'errstr': e.args[0],
                }
            self.response.headers['Content-Type'] = 'text/json'
            json.dump( reply, self.response.out )
            return
        else:
            reply = {
                    'status': "ok",
                    'result': result,
                }
            self.response.headers['Content-Type'] = 'text/json'
            json.dump( reply, self.response.out )
            return

    def fetch(self, url ):

        if not url:
            raise FetchError, "missing url"

        try:
            res = fetch( url )
        except InvalidURLError, e:
            raise FetchError, "invalid url"
        except DownloadError, e:
            raise FetchError, "unable to download"
        except:
            raise FetchError, "unknown error"

        soup = BeautifulSoup( res.content )
        extractor = poll.Extractor( soup )

        polls = extractor.detect()

        for i, p in enumerate(polls):
            for s in p[7]: #specials
                if s[3] is None: # specialtype
                    del polls[i]
                    break

        if len(polls) < 1:
            raise FetchError, "no poll found"

        if len(polls) > 1:
            polls = [polls[0],]
            """
            dpolls = map( poll2dict, polls )
            for d in dpolls:
                del d['hiddens']
                del d['specials']
            result = {
                    'type': "multiple",
                    'msg': "Multiple polls found.",
                    'count': len(polls),
                    'polls': dpolls,
                }
            return result
            """

        p = poll2dict( polls[0] )

        body = """
<div class="poll">
    <strong>Poll found!</strong>
    <table class="pollinfo">
        <caption>Poll Information</caption>
        <tbody>
            <tr><td>Form ID:</td><td>%s</td></tr>
            <tr><td>Form Name:</td><td>%s</td></tr>
            <tr><td>Action:</td><td>%s</td></tr>
            <tr><td>Method:</td><td>%s</td></tr>
            <tr><td>Number of choices:</td><td>%d</td></tr>
        </tbody>
    </table>
    <p>Please select the poll option to vote on:</p>
    <div class="choices">{radios}</div>
    <a href="#" class="submit">vote!</a>
</div>
"""
        content = body % (
                p['id'], p['name'], p['action'],
                p['method'] or "get", len(p['choices']),
            )

        radios = ""
        for i, c in enumerate(p['choices']):
            if c[1]:
                name = c[1]
            elif c[0]:
                name = c[0]
            else:
                name = "#%02d" % i
            radios += """
            <div class="choice"><input type="radio" name="choice" value="%d" /> %s
            </div>""" % (i, name )
        content = content.replace( "{radios}", radios )
        content = ' '.join(content.split())

        result = {
                'type': "fetched",
                'msg': "Poll found.",
                'html': content,
            }

        return result


# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

