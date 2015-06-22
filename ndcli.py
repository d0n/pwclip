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

from colortext import fatal
from systools import which
from executor import command as c
from dpkg import DePyKG
from network import askdns

# global default variables
__version__ = '0.0'

def ndcli(pattern):
	if not DePyKG().isinstalled('ui-ndcli'):
		fatal('packet', 'ui-ndcli', 'is not installed')
	ndcli = which('ndcli')
	def __ndclicmd(pattern):
		ndclicmd = None
		isip = re.search('^(\d{1,3}\.){3}\d{1,3}$', pattern)
		isnet = re.search('^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$', pattern)
		if isip:
			if pattern.endswith('.0') or isnet:
				error(
				    'entered pattern', pattern,
				    'is a netaddress but no mask defined')
				print(blu('trying to guess...'))
				ip = re.sub(r'\d$', '1', pattern)
				out = c.stdx(ndcli+' show ip '+str(ip))
				for line in str(out).split('\\n'):
					if 'subnet' in line:
						return '%s list pools %s'%(ndcli, line.split(':')[1])
			else:
				return '%s show ip %s'%(ndcli, pattern)
		else:
			ip = askdns(pattern)
			if ip:
				return '%s show ip %s'%(ndcli, ip)
			return '%s list pools %s'%(ndcli, pattern)
	cmd = __ndclicmd(pattern)
	return c.stdo(cmd)









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
