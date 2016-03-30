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
    basename as _basename, \
    dirname as _dirname, \
    expanduser as _expanduser, \
    isdir as _isdir, \
    isfile as _isfile

class PasswordListParser(object):
	_dbg = False
	_pwlist = []
	_listfile = ''
	def __init__(self, listfile):
		self.listfile = listfile
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

	@property                # listfile <str>
	def listfile(self):
		return self._listfile
	@listfile.setter
	def listfile(self, val):
		if val.startswith('~'):
			val = _expanduser(val)
		if not _isdir(_dirname(val)):
			raise FileNotFoundError(val)
		if _isfile(val):
			with open(val, 'r') as pwf:
				self._pwlist = [l.strip() for l in pwf.readlines()]
		self._listfile = val

	@property                # pwlist <list>
	def pwlist(self):
		return self._pwlist

	
