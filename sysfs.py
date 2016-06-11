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
"""sysfs wrapper"""
# global imports
import re
import os
import sys

# default constant definition
__version__ = '0.3'

class SysFs:
	_path_ = '/sys'
	__dict__ = {}
	def __init__(self, path='/sys'):
		if not os.path.isdir('/sys'):
			raise RuntimeError('directory /sys could not be found')
		self._path_ = os.path.realpath(path)
		if not self._path_.startswith('/sys/') and not '/sys' == self._path_:
			raise RuntimeError(
			    'cannot apply on non-sysfs path %s'%(self._path_))
		self.__dict__.update(dict.fromkeys(os.listdir(self._path_)))

	def __repr__(self):
		return '<sysfs.Node "%s">'%self._path_

	def __setattr__(self, name, val):
		if name.startswith('_'):
			return object.__setattr__(self, name, val)
		path = os.path.realpath(os.path.join(self._path_, name))
		if os.path.isfile(path):
			with open(path, 'w') as fp:
				fp.write(str(val))
		else:
			raise RuntimeError('Cannot write to non-files.')

	def __getattribute__(self, name):
		if name.startswith('_'):
			return object.__getattribute__(self, name)
		path = os.path.realpath(os.path.join(self._path_, name))
		if os.path.isfile(path):
			with open(path, 'r') as fp:
				data = fp.read().strip()
			try:
				return int(data)
			except ValueError:
				return data
		elif os.path.isdir(path):
			return SysFs(path)

	def __setitem__(self, name, val):
		return setattr(self, name, val)

	def __getitem__(self, name):
		return getattr(self, name)

	def __iter__(self):
		return iter(os.listdir(self._path_))










if __name__ == '__main__':
	"""display all classes/definitions which are imported/defined (disabled)"""
	"""
	for func in dir(sys.modules[__name__]):
		if not '-v' in sys.argv:
			if str(func).startswith('__') or func == 'func':
				continue
		print(func)
		if func in sys.argv:
			print(dir(func))
			continue
	print()
	"""
	sfs = SysFs('/sys/class')
	#print([f for f in sfs.fs.__iter__()])
	#print([p for p in sfs.__iter__()])
	#sys._path_ = '/sys/class'
	#print([p for p in sfs.__iter__()])
