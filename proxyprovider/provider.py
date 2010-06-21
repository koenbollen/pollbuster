#!/usr/bin/env python
from collections import namedtuple
import urllib2
#from BeautifulSoup import BeautifulSoup
import re
from pprint import pprint
import sys

proxy = namedtuple( "proxy", "host port type source" )

rx_proxy = re.compile( r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})')
rx_jsproxy = re.compile( r'proxy\((\d+),\'(\d+)\',\'(\d+)\',\'(\d+)\',\'(\d+)\',(\d+)\);')


providers = []

def provider( cls ):
	providers.append(cls)
	return cls

def parse_with_regex(data,type,source):
	result = []
	for ip,port in rx_proxy.findall(data):
		try:
			port = int(port)
		except ValueError:
			continue
		result.append(proxy(ip,port,type,source))
	return result

@provider
def haozs():
	result = []
	urlbase = 'http://www.haozs.net/ip%d.htm'
	page = 1
	while True:
		try:
			r = parse_with_regex(download(urlbase%page),'http','haozs')
			if len(r) == 0:
				break
			result += r
			page += 1
		except:
			print 'breaking at', urlbase%page
			break
	return result

@provider
def samairru():
	result = []
	url = 'http://www.samair.ru/proxy/socks.htm'
	urlbase = 'http://www.samair.ru/proxy/socks%d.htm'
	page = 2
	result += parse_with_regex(download(url),'socks','samairru')
	try:
		while True:
			r = parse_with_regex(download(url),'socks','samairru')
			page += 1
			if len(r) == 0:
				break
			result += r
	except:
		pass

	return result


@provider
def proxyforest():
	result = []
	baseurl = 'http://www.proxyforest.com/e-proxy.htm?pages=%d'
	page = 0
	found = True
	while found:
		found = False
		data = download(baseurl%page)
		for jspr in rx_jsproxy.findall(data):
			ip,port = {
					'1': lambda d: ("%s.%s.%s.%s"%(d[0],d[1],d[2],d[3]),int(d[4])),
					'2': lambda d: ("%s.%s.%s.%s"%(d[3],d[0],d[1],d[2]),int(d[4])),
					'3': lambda d: ("%s.%s.%s.%s"%(d[2],d[3],d[0],d[1]),int(d[4])),
					'4': lambda d: ("%s.%s.%s.%s"%(d[1],d[2],d[3],d[0]),int(d[4])),
					}[jspr[0]](jspr[1:])
			result.append(proxy(ip,port,'http','proxyforest'))
			found = True
		page += 1
	return result

@provider
def proxywowag():
	result = []
	baseurl = 'http://proxy.wow.ag/proxybyPerformance.php?offset=%d'
	offset = 0
	while True:
		try:
			data = download(baseurl%offset)
			r = parse_with_regex(data,'http','proxywowag')
			if len(r) == 0:
				break
			result += r
			offset += len(r)
		except urllib2.HTTPError:
			break
	return result

@provider
def proxyipncorg():
	result = []
	urls = ['http://proxy.ipcn.org/proxylist.html','http://proxy.ipcn.org/proxylist2.html']
	for url in urls:
		try:
			pys = download(url)
			result += parse_with_regex(pys,'http','proxyipncorg')
		except urllib2.HTTPError:
			continue
	return result

@provider
def compinforu():
	url = 'http://comp-info.ru/proxy/'
	pys = download(url)
	pys = pys[pys.index('textarea'):]
	pys = pys[pys.index('>')+1:]
	pys = pys[0:pys.index('<')]
	pys = pys.splitlines()
	result = []
	for p in pys:
		if ':' not in p:
			continue
		host,port = p.split(':',1)
		try:
			port = int(port)
		except ValueError:
			continue
		result.append(proxy(host.strip(),port,'http','compinforu'))
	return result

@provider
def proxylistsnet():
	result = []
	urls = [
			('http://www.proxylists.net/http.txt','http'),
			('http://www.proxylists.net/http_highanon.txt','http'),
			('http://www.proxylists.net/socks4.txt','socks4'),
			('http://www.proxylists.net/socks5.txt','socks5'),
			]
	for url,type in urls:
		response = urllib2.urlopen(url)
		pys = download(url).splitlines()
		for p in pys:
			if ':' not in p:
				continue
			host,port = p.split(':',1)
			try:
				port = int(port)
			except ValueError:
				continue
			result.append(proxy(host.strip(),port,type,'proxylistsnet'))
	return result

def download(url):
		opener = urllib2.build_opener()
		opener.addheaders = [
				('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.70 Safari/533.4'),
				('Accept','application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
				('Accept-Language','nl-NL,nl;q=0.8,en-US;q=0.6,en;q=0.4'),
				('Accept-Charser','Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3')
				]
		return opener.open(url).read()

def main():
	#global providers
	proxies = []
	for p in providers:
		try:
			proxies += p()
		except urllib2.HTTPError:
			continue

	pprint( proxies )
	print 'length',len(proxies)

if __name__ == "__main__":
    main()

