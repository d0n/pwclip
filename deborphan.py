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
#import re
import os
import sys

# local relative imports
sys.path = [os.path.expanduser('~/bin')] + [p for p in sys.path if (
    not p == os.path.expanduser('~/bin'))]
from modules.colortext import blu
from modules.system.executor import Command
from modules.system.common import which


# global default variables
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.path.abspath(os.readlink(os.path.dirname(__file__)))
__version__ = '0.0'


def orphan(server, background=None, debug=None):
	if debug:
		print(orphan)
	c = Command(dbg=debug, host=server, user='root')
	xce = c.call
	if background:
		xce = c.erno
	if int(
	      c.erno('dpkg -s deborphan')
	      ) != 0:
		xce('aptitude -y install deborphan')
	orphpks = c.stdo('deborphan |tr "\n" " "')
	legacys = c.stdo('dpkg -l |grep "^rc.*" |awk \'{print $2}\' |tr "\n" " "')
	pkgs = []
	if orphpks:
		pkgs = orphpks.split(' ')
	if legacys:
		pkgs = pkgs + legacys.split(' ')
	if pkgs:
		if int(xce('aptitude -y purge %s'%(' '.join(p for p in pkgs)))) == 0:
			return pkgs
	








if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
