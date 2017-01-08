#!/usr/bin/env python3
"""package managing modue"""

#global imports
import os
import sys

#local relative imports
from system import which
from executor import sucommand as sudo
from colortext import bgre, tabd

from deb.dpkg import DePyKG

# default constant definitions
__version__ = '0.1'

class Apytude(DePyKG):
	# external properties
	su_ = True
	sh_ = True
	# common/internal properties
	aptopts = []
	dbg = None
	dry = None
	vrb = None
	aptbin = which('apt')
	def __init__(self, *args, **kwargs):
		#DePyKG.__init__(self, *args, **kwargs)
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(Apytude.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	def search(self, pattern=''):
		if self.dbg:
			print(bgre(self.search))
		return self.stdx(self.aptbin, self.aptopts, 'search', pattern)

	def update(self):
		if self.dbg:
			print(bgre(self.update))
		if sudo.call(self.aptbin, 'update') == 0:
			return True

	def upgrade(self, mode='upgrade'):
		if self.dbg:
			print(bgre(self.upgrade))
		opts = ''
		if self.aptopts:
			opts = '-'+''.join(opt for opt in self.aptopts)
		if mode in ('full', 'dist'):
			mode = 'dist-upgrade'
		command = '%s %s %s' %(self.aptbin, opts, mode)
		if sudo.call(command) == 0:
			return True

	def install(self, packages, opts=''):
		if self.dbg:
			print(bgre(self.install))
		if self.dry:
			self.aptopts.append('s')
		if opts:
			opts = '-%s'%(
                ' -'.join(opt for opt in opts.split(' ')))
		if self.aptopts:
			opts = '%s %s'%(
                opts, ' -'.join(opt for opt in self.aptopts))
		if packages:
			packages = self._list(packages)
			packages = ' '.join(
                pkg for pkg in packages if not self.isinstalled(pkg))
		if not packages and not 'f' in opts:
			return
		command = '%s %s install %s' %(self.aptbin, opts, packages)
		erno = sudo.call(command)
		if int(erno) == 0:
			return packages
		else:
			return erno

	def purge(self, packages, opts=''):
		if self.dbg:
			print(bgre(self.purge))
		if opts:
			opts = '-%s'%(
                ' -'.join(opt for opt in opts.split(' ')))
		if self.aptopts:
			opts = '%s %s'%(
                opts, ' -'.join(opt for opt in self.aptopts))
		if packages:
			packages = ' '.join(
                pkg for pkg in packages if self.isinstalled(pkg))
		if not packages and not 'f' in opts:
			return
		command = '%s %s purge %s' %(self.aptbin, opts, packages)
		erno = sudo.call(command)
		if int(erno) == 0:
			return packages
		else:
			return erno

	def autoclean(self, opts=''):
		if self.dbg:
			print(bgre(self.purge))
		if opts:
			opts = '-%s'%(
                ' -'.join(opt for opt in opts.split(' ')))
		if self.aptopts:
			opts = '%s %s'%(
                opts, ' -'.join(opt for opt in self.aptopts))
		self.purge(self.partlyinstalleds(), opts='-y')
		command = '%s %s autoremove'%(self.aptbin, opts)
		return int(self.call(command))





if __name__ == '__main__':
	print('\n'.join(m for m in dir()))
	apt = AptSource('dbg')
	print(apt.srces)
