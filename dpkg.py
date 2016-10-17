#!/usr/bin/env python3
"""package managing modue"""

#global imports
import os
import sys

#local relative imports
from system import which
from executor import Command
from colortext import bgre

# default constant definitions
__version__ = '0.1'

class DePyKG(Command):
	_pkgbin = which('dpkg')
	@property # pkgbin <str>
	def pkgbin(self):
		return self._pkgbin

	def isinstalled(self, package):
		if self.erno(self.pkgbin, '-s', package) == 0:
			return True



if __name__ == '__main__':
	exit(1)
