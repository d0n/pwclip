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
	_ato = False
	_branchs = []
	def __init__(self, *args, **kwargs):
		self._ato = True
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
		if self._dbg:
			print(GitRepo.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
	@property               # ato <bool>
	def ato(self):
		return self._ato
	@ato.setter
	def ato(self, val):
		self._ato = val if type(val) is bool else self._ato
	@property               # branchs <list>
	def branchs(self):
		return self._branchs
	@branchs.setter
	def branchs(self, val):
		self._branchs = val if type(val) is list else self._branchs

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
