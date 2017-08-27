#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""net.dns module"""

try:
	from os import uname
except ImportError:
	from os import environ
	uname = ['', environ['COMPUTERNAME']]

from socket import getfqdn, gethostbyaddr, gaierror, herror

from net.isip import isip

def fqdn(name):
	"""get the fully qualified domain name"""
	__fqdn = getfqdn(name) if name else uname()[1]
	if __fqdn:
		return __fqdn
	return name

def askdns(host):
	"""ask dns for ip or name and return answer if ther is one"""
	try:
		dnsinfo = gethostbyaddr(host)
	except (gaierror, herror, TypeError):
		return
	if isip(host):
		return dnsinfo[0]
	if len(dnsinfo[2]) == 1:
		return dnsinfo[2][0]
	return dnsinfo[2]

def raflookup(host):
	"""reverse and forward lookup function"""
	if host:
		lookup = askdns(host)
		if lookup:
			reverse = askdns(lookup)
			return lookup, reverse
