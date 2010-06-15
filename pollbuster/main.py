#!/usr/bin/env python
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from index import IndexPage

from polls import ExtactAjax

application = webapp.WSGIApplication(
        [
            ('/', IndexPage),
            ('/poll.extract', ExtactAjax),
        ],
        debug=True
    )

def main():
    run_wsgi_app( application )

if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

