#!/usr/bin/env python3
"""package managing modue"""

#global imports
import os
import sys

#local relative imports
from system import which
from executor import Command
from colortext import bgre, tabd

# default constant definitions
__version__ = '0.1'


class DePyKG(Command):
	dbg = None
	_pkgbin = which('dpkg')
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(DePyKG.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property # pkgbin <str>
	def pkgbin(self):
		return self._pkgbin

	def isinstalled(self, package):
		if self.erno(self.pkgbin, '-s', package) == 0:
			return True

	def partlyinstalleds(self):
		return [d for d in self.stdo(
            self.pkgbin, '-l').split('\n') if d.startswith('rc')]


if __name__ == '__main__':
	exit(1)
