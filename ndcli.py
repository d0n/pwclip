#!/usr/bin/env /usr/bin/python3
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""module disclaimer"""
# global & stdlib imports
import re
import os
import sys

from system import which
from colortext import error, fatal, blu
from executor import command as c
from net import askdns
from deb import DePyKG

# global default variables
__version__ = '0.1'

def ndcli(pattern):
	#if not DePyKG().isinstalled('ui-ndcli'):
	#	fatal('packet', 'ui-ndcli', 'is not installed')
	ndclibin = which('ndcli')
	def __ndclicmd(pattern):
		ndclicmd = ''
		isip = re.search(r'^(\d{1,3}\.){3}\d{1,3}$', pattern)
		isnet = re.search(r'^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$', pattern)
		if isip:
			if pattern.endswith('.0') or isnet:
				error('entered pattern ', pattern, \
                    ' is a netaddress but no mask defined')
				print(blu('trying to guess...'))
				ip = re.sub(r'\d$', '1', pattern)
				out = c.stdx('%s show ip %s'%(ndclibin, ip))
				for line in str(out).split('\\n'):
					if 'subnet' in line:
						return '%s list pools %s'%(ndclibin, line.split(':')[1])
			else:
				return '%s show ip %s'%(ndclibin, pattern)
		else:
			ip = askdns(pattern)
			if ip:
				return '%s show ip %s'%(ndclibin, ip)
			return '%s list pools %s'%(ndclibin, pattern)
	cmd = __ndclicmd(pattern)
	return c.stdo(cmd)









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
