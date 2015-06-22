#!/usr/bin/env /usr/bin/python3
#
# This file is free software by  <- d0n - d0n@janeiskla.de ->
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
#import re
import os
import sys
import time

# local relative imports
from colortext import abort
from executor import Command

# global default variables
__version__ = '0.0'

def kvntool(modes, hostgroups=':all'):
	ssh = Command(
	    'sh_',
	    **{'user': 'keys', 'host': 'keyverteiler-neu.schlund.de'}
	    )
	def __distribute(hostgroup):
		if not hostgroup.startswith('hg:') and not hostgroup == ':all':
			hostgroup = 'hg:%s'%(hostgroup)
		cmd = 'distribute %s'%(hostgroup)
		return ssh.call(cmd)

	for mod in ('export', 'make', 'distribute'):
		if mod in modes:
			if mod == 'distribute':
				if hostgroups != ':all':
					if type(hostgroups) in (list, tuple):
						for hostgroup in hostgroups:
							__distribute(hostgroup)
					elif type(hostgroups) is str:
						__distribute(hostgroups)
				else:
					__distribute(hostgroups)
			else:
				ssh.call(mod)








if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
