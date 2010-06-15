#!/usr/bin/env python
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL

import re
import urllib2

url = "http://www.kleimo.com/random/name.cfm"
post = "type=3&number=%d&obscurity=20&Go=1"

rx = re.compile( r"\d+\. &nbsp; (\w+ \w+)<br>" )

def download( n=10 ):
    req = urllib2.urlopen( url, post%n )
    data = req.read()
    req.close()

    return rx.findall( data )

def main():
    out = open( "names.txt", "ab" )
    for name in download():
        print >>out, name.strip()
    out.close()

if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

