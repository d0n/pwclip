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
"""mount wrapping module"""

# global & stdlib imports
#import re
import os
import sys

# local relative imports
from colortext import bgre
from .blkid import BlockDevices

# global default variables
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.path.abspath(os.readlink(os.path.dirname(__file__)))
__version__ = '0.0'

class DeviceMounter(BlockDevices):
	_sh_ = True
	_dbg = None
	_base = os.path.expanduser('~/mnt')
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
			print(bgre('%s\n%s'%(
			    Mounter.__mro__,
			    ''.join('%s = %s'%(k, v) for (k, v) in self.__dict__.items())
			    )))
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg

	@property               # base <str>
	def base(self):
		return self._base
	@base.setter
	def base(self, val):
		self._base = val if type(val) is str else self._base

	def _makedir(self, path):
		if os.path.islink(path):
			path = os.path.readlink(path)
		if not os.path.isdir(path):
			try:
				os.makedirs(path)
			except OSError as err:
				print(
                    'destination "%s" exists but is a file'%path,
                    file=sys.stderr)







if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	mc = Mounter('dbg')
	print(mc._mounteds())
