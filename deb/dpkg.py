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
	pkgbin = which('dpkg')
	_packages = []
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
		args = args + ['su_', 'sh_']
		Command().__init__(*args, **kwargs)

	@property                # packages <type>
	def packages(self):
		if self.dbg:
			print(bgre(self.packages))
		if self._packages:
			return self._packages
		plst = self.stdo(self.pkgbin, '-l')
		pkgs = {}
		for p in plst.split('\n'):
			p = p.split()
			if not p or len(p) < 5:
				continue
			pkgs[p[1].split(':')[0]] = {
                'status': p[0],
                'version': p[2],
                'architecture': p[4],
                'description': ' '.join(p[5:])}
		self._packages = pkgs
		return self._packages

	def isinstalled(self, package):
		if self.dbg:
			print(bgre(self.isinstalled))
		if package in self.packages.keys():
			return True
		ppart = None
		if package.endswith('-dev'):
			ppart = package.rstrip('-dev')
		for pkg in self.packages.keys():
			if ppart and pkg.startswith(ppart) and pkg.endswith('-dev'):
				return True

	def partlyinstalleds(self):
		if self.dbg:
			print(bgre(self.partlyinstalleds))
		return [p for (p, ifs) in self.packages.items() \
            if ifs['status'] == 'rc']


if __name__ == '__main__':
	exit(1)
