#!/usr/bin/env python3
"""package managing modue"""

#global imports
import os
import sys

#local relative imports
from system import which
from executor import Command
from colortext import bgre, tabd


class DePyKG(Command):
	dbg = None
	_pkgbin = which('dpkg')
	co = Command('sh_').stdo
	packages = [p.split() for p in co(_pkgbin, '-l').split('\n') if p]
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(DePyKG.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property # pkgbin <str>
	def pkgbin(self):
		return self._pkgbin

	def isinstalled(self, package):
		if self.dbg:
			print(bgre(self.isinstalled))
		for pkg in self.packages:
			if len(pkg) < 2:
				continue
			if pkg[1].split(':')[0] == package:
				return True

	def partlyinstalleds(self):
		return [p[1] for p in  self.packages if p and p[0] == 'rc']


if __name__ == '__main__':
	exit(1)
