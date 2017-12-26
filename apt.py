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

class Apytude(DePyKG):
	# external properties
	su_ = True
	sh_ = True
	# common/internal properties
	dbg = None
	dry = None
	vrb = None
	opts = []
	aptbin = which('apt')
	_distname = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(Apytude.__mro__))
			print(bgre(tabd(Apytude.__dict__, 2)))

	@property                # distname <str>
	def distname(self):
		if not self._distname:
			with open('/etc/lsb-release', 'r') as lfh:
				self._distname = [
                    l.split('=')[1].strip() for l in lfh.readlines() \
                        if l.startswith('DISTRIB_CODENAME')][0]
		return self._distname

	def srcupdate(self, url, key, dist=None):
		if self.dbg:
			print(self.srcupdate)

	def search(self, pattern=''):
		if self.dbg:
			print(bgre(self.search))
		return self.stdx(self.aptbin, self.aptopts, 'search', pattern)

	def update(self):
		if self.dbg:
			print(bgre(self.update))
		if sudo.call(self.aptbin, 'update') == 0:
			return True

	def upgrade(self, *opts):
		if self.dbg:
			print(bgre(self.upgrade))
		opts = opts if opts else self.opts
		if opts:
			opts = '-%s'%' -'.join(opts)
		opts = '' if not opts else opts
		command = '%s %s upgrade' %(self.aptbin, opts)
		if sudo.call(command) == 0:
			return True

	def install(self, packages, *opts):
		if self.dbg:
			print(bgre(self.install))
		if self.dry:
			self.aptopts.append('s')
		if opts:
			opts = '-%s'%' -'.join(opts)
		opts = '' if not opts else opts
		packages = self._list(packages)
		packages = ' '.join(p for p in packages if not self.isinstalled(p))
		if not packages and not 'f' in opts:
			return
		#print(packages)
		command = '%s %s install %s' %(self.aptbin, opts, packages)
		erno = sudo.call(command)
		if int(erno) == 0:
			return packages
		else:
			return erno

	def purge(self, packages, *opts):
		if self.dbg:
			print(bgre(self.purge))
		opts = opts if opts else self.opts
		if opts:
			opts = '-%s'%' -'.join(opts)
		opts = '' if not opts else opts
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

	def autoclean(self, *opts):
		if self.dbg:
			print(bgre(self.purge))
		opts = opts if opts else self.opts
		self.purge(self.partlyinstalleds(), *opts)
		if opts:
			opts = '-%s'%' -'.join(opts)
		opts = '' if not opts else opts
		command = '%s %s autoremove'%(self.aptbin, opts)
		return int(self.call(command))






if __name__ == '__main__':
	exit(1)
