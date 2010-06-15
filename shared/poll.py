#!/usr/bin/env python
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL


import sys
from collections import namedtuple
import random

class PollError( Exception ):
    pass

class InvalidPollError( PollError ):
    pass

Poll = namedtuple( 
        "Poll",
        "id name method action groupname choices hiddens specials"
    )
Hidden = namedtuple( "Hidden", "name value" )
Input = namedtuple( "Input", "type name value special" )

class Extractor( object ):

    def __init__(self, soup ):
        self.soup = soup

    def detect(self ):
        polls = []
        for form in self.soup.findAll( "form" ):
            try:
                polls.append( self.parse( form ) )
            except PollError, e:
                pass
        return polls

    def parse(self, form ):
        id = form.get("id")
        name = form.get("name")
        method = form.get("method")
        if method:
            method = method.strip().lower()
        action = form.get("action")

        choices = []
        hiddens = []
        specials = []

        names = set()
        radios = form.findAll( "input", type="radio" )
        for radio in radios:
            try:
                names.add( radio['name'] )
            except KeyError:
                continue
        if len(names) == 0:
            raise InvalidPollError( "no radio group found" )
        if len(names) > 1:
            raise InvalidPollError( "more the one radio group found" )
        groupname = names.pop()

        radios = filter( lambda x: x.get("name")==groupname, radios )
        if len(radios) < 2:
            raise InvalidPollError( "less the 2 radio fields" )
        for radio in radios:
            try:
                value = radio['value']
            except KeyError:
                continue
            text = None
            if radio.get("id"):
                label = form.find( "label", {'for':radio['id']} )
                if label:
                    while label and label.string is None:
                        label = label.next
                    if label:
                        text = label.string
            if text is None:
                if radio.next.string is not None and radio.next.string.strip():
                    text = radio.next.string.strip()
            choices.append( (value, text) )

        for hid in form.findAll( "input", type="hidden" ):
            try:
                hiddens.append( Hidden(hid['name'], hid.get("value")) )
            except KeyError:
                pass

        inputs = form.findAll( "input", {'type':("text","password")} )
        for i in inputs:
            try:
                type = i['type']
                name = i["name"]
                lname = name.lower()
                value = i.get("value")
                special = None
                for s in availible_specials:
                    for n in s.names:
                        if n in lname:
                            special = s
                            break
                    if special is not None:
                        break
                specials.append( Input(
                        type,
                        name,
                        value,
                        special,
                    ) )
            except KeyError:
                pass

        submit = form.find( "input", type="submit" )
        if submit:
            try:
                specials.append( Input( "submit", submit['name'],
                    submit.get("value"), None ) )
            except KeyError:
                pass

        return Poll(
                id, name, method, action, 
                groupname, choices,
                hiddens, specials
            )

class Special( object ):
    names = None
    valuetype = "constant"

    def generate_value(self ):
        return None

class NameSpecial( Special ):

    names = ("name", "n")
    valuetype = "cyclic"

    def  __init__(self, filename=None ):
        if filename:
            try:
                inf = open( filename )
                self.names = inf.readlines()
            except IOError:
                filename = None
        if not filename:
            import names
            self.names = names.download(100)
        self.count = 0

    def generate_value(self ):
        name = self.names[self.count]
        self.count += 1
        self.count %= len(self.names)
        return name

    def __repr__(self ):
        return "name"

class MailSpecial( Special ):

    names = ( "mail", "addr" )
    valuetype = "random"

    def generate_value(self, ):
        name = random.sample( "abcdefghijklmnopqrstuvwxyz", 8 )
        return "".join(name) + "@dispostable.com"

    def __repr__(self ):
        return "mail"

availible_specials = ( NameSpecial, MailSpecial )

def main():
    from BeautifulSoup import BeautifulSoup
    from pprint import pprint
    soup = BeautifulSoup( open("poll_usecase.html").read() )
    ext = Extractor( soup )
    polls = ext.detect()
    pprint( polls )
    print polls[-1].specials[0].special().generate_value()

if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:

