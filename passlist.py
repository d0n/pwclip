#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""password list parsing library"""
# (std)lib imports
from os.path import \
    isdir as _isdir, \
    isfile as _isfile, \
    dirname as _dirname, \
    basename as _basename, \
    expanduser as _expanduser



class PasswordListParser(dict):
	_dbg = False
	_usrpwds = {}
	def __init__(self, usrpwds):
		self._usrpwds = 
		if self.dbg:
			lim = int(max(len(k) for k in PasswordListParser.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                PasswordListParser.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(PasswordListParser.__dict__.items())),
                PasswordListParser.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	@property                # usrpwds <dict>
	def usrpwds(self):
		return self._usrpwds

	def search(self, pattern):
		for (usr, pwd) in self.usrpwds.items():
			if pattern in usr:
				yield pwd
			elif pattern in pwd:
				yield usr



