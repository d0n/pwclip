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

from colortext import blu, bgre
from net import SecureSHell as SSH


def orphan(server, background=None, debug=None):
	if debug:
		print(bgre(orphan))
	ssh = SSH(*[a for a in ['dbg' if debug else None] if a],
        **{'remote': server, 'reuser': 'root'})
	xce = ssh.call
	if background:
		xce = ssh.erno
	if ssh.erno('dpkg -s deborphan') != 0:
		xce('apt-get -y install deborphan')
	orphpks = ssh.stdo('deborphan |tr "\n" " "')
	confdps = ssh.stdo('dpkg -l |grep "^rc.*" |awk \'{print $2}\' |tr "\n" " "')
	pkgs = []
	if orphpks:
		pkgs = orphpks.split(' ')
	if confdps:
		pkgs = pkgs + confdps.split(' ')
	atocpks = ssh.stdo('apt-get -y autoremove')
	pkgs = pkgs + [
        i.split(' ')[1].strip() for i in atocpks.split('\n') \
        if i.startswith('Removing ')]
	if int(xce('apt-get -y purge %s'%(' '.join(p for p in pkgs)))) == 0:
		if pkgs:
			return pkgs









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
