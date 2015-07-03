#!/usr/bin/env python3
"""repo common functions module"""
# global imports
import os
import sys

# local relative imports
from .git import GitSync

# default vars
__version__ = '0.0'

class RepoSync(GitSync):
	sh_ = True
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
			lim = int(max(len(k) for k in RepoSync.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                RepoSync.__mro__,
                '\n'.join('  %s%s=\t%s'%(
                    k, ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(RepoSync.__dict__.items())),
                RepoSync.__init__,
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
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg

	def sync(self, repo):
		if os.path.exists(repo):
			os.chdir(repo)
			if os.path.isdir(repo+'/.git'):
				self.gitsync()
			if os.path.isdir(repo+'/.svn'):
				c.call('svn up')
			if os.path.isdir(repo+'/CVS'):
				c.call('cvs up -d -P')






if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
