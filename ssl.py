#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""ssl lib"""

from os import path
import sys

from subprocess import call

from executor import command as x
from secrecy import GPGTool

gpg = GPGTool('dbg')

def pem2p12(key, cert, out=None):
	out = out if out else '%s.p12'%path.basename(key).split('.')[0]
	x.stdo('openssl pkcs12 -export -in %s -inkey %s -out %s'%(cert, key, out))
	x.call('gpgsm --import %s'%out)
	key = ''
	for ln in x.stdo('gpgsm -K').split('\n'):
		ln = ln.strip()
		if ln.startswith('ID:'):
			key = ln.split(': ')[1]
			x.stdo('gpgsm -o %s.pem --export-secret-key-p12 %s'%(key, key))
			print(key)
			print(x.stdo('gpg2 --allow-secret-key-import --import %s.pem'%key))
