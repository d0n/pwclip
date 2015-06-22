#!/usr/bin/env python3
"""package managing modue"""

#global imports
import os
import sys

#local relative imports
from .misctools import which

from executor import Command

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

'''
class Apytude(Command):
	_dbg = False
	_dry = False
	_vrb = False
	_su_ = False
	_sh_ = False
	_aptopts = []
	_aptbin = which('aptitude')
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(args)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(Apytude.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
			print()
		super().__init__(*args, **kwargs)
	# rw properties
	@property
	def dbg(self): #dbg <bool>
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if val is bool else self._dbg
	@property
	def dry(self): #dry <bool>
		return self._dry
	@dry.setter
	def dry(self, val):
		self._dry = val if val is bool else self._dry
	@property
	def vrb(self): #vrb <bool>
		return self._vrb
	@vrb.setter
	def vrb(self, val):
		self._vrb = val if val is bool else self._vrb
	@property
	def aptbin(self): # aptbin <str> & which(str)
		return self._aptbin
	@aptbin.setter
	def aptbin(self, val):
		self._aptbin = val if which(val) else self._aptbin
	@property
	def aptopts(self):
		return self._aptopts
	@aptopts.setter
	def aptopts(self, vals):
		self._aptopts = [val for val in vals]\
		  if type(vals) in (list, tuple)\
		  else [vals]

	def search(self, pattern=''):
		return self.stdx(self.aptbin, self.aptopts, 'search', pattern)

	def update(self):
		if int(self.stdx(self.aptbin, 'update')) == 0:
			return True

	def upgrade(self, mode):
		opts = ''
		if self.aptopts:
			opts = '-'+''.join(opt for opt in self.aptopts)
		action = 'upgrade'
		if mode in ('full', 'dist'):
			action = 'full-upgrade'
		command = '%s %s %s' %(self.aptbin, opts, action)
		if int(self.stdx(command)) == 0:
			return True

	def install(self, *packages, opts=''):
		if self.dry:
			self.aptopts.append('s')
		opts = ''
		if opts:
			opts = ' -'.join(opt for opt in opts)+' -'.join(opt for opt in self.aptopts)
		packages = ''
		if packages:
			dpkg = DePyKG()
			packages = ' '.join(pkg for pkg in packages if not dpkg.isinstalled(pkg))
		if not packages or not 'f' in opts:
			return
		command = '%s %s install %s' %(self.aptbin, opts, packages)
		erno = self.stdx(command)
		if int(erno) == 0:
			return packages
		else:
			return erno

	def purge(self, *packages, opts=''):
		dpkg = DePyKG()
		opts = ''
		if self.aptopts:
			opts = ' -'.join(opt for opt in self.aptopts)
		if packages:
			packages = ' '.join(pkg for pkg in packages if dpkg.isinstalled(pkg))
		if not packages or not 'f' in opts:
			return
		command = '%s %s pruge %s' %(self.aptbin, opts, packages)
		erno = self.stdx(command)
		if int(erno) == 0:
			return packages
		else:
			return erno





if __name__ == '__main__':
	print('\n'.join(m for m in dir()))
	apt = AptSource('dbg')
	print(apt.srces)

'''
