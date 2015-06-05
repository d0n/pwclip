#!/usr/bin/env python3
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
"""user module provides systems user information"""
# global & stdlib imports
import os


class Users(object):
	_dbg = False
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in Users.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
			    Users.__mro__,
			    '\n'.join('  %s%s=\t%s'%(
			        k, ' '*int(lim-len(k)), v
			    ) for (k, v) in sorted(Users.__dict__.items())),
			    Users.__init__,
			    '\n'.join('  %s%s=\t%s'%(k[1:], ' '*int(
			        int(max(len(i) for i in self.__dict__.keys())+4
			        )-len(k)), v
			    ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@staticmethod
	def _passwd():
		with open('/etc/passwd', 'r') as pwd:
			return pwd.readlines()
	@staticmethod
	def _groups():
		with open('/etc/groups', 'r') as grp:
			return grp.readlines()
	@property                # name <str>
	def name(self):
		for line in self._passwd():
			if int(line.split(':')[2]) == int(os.getuid()):
				return line.split(':')[0].strip()




if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	user = Users('dbg')
	print(user.name)
