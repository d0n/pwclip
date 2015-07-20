#!/usr/bin/env python3
"""repo common functions module"""
# global imports
<<<<<<< HEAD
import os
import sys

# local relative imports
from modules.lib.colortext import blu, yel

from modules.repo import GitSync
=======
from os import listdir as _listdir, chdir as _chdir
from os.path import exists as _exists, isdir as _isdir

# local relative imports
from lib.colortext import blu, yel
from .subversion import SubVersion

from .git import GitSync
>>>>>>> 3cabfc8e133237046ff5fb204d59ccde90c8af7d

# default vars
__version__ = '0.1'

class RepoSync(GitSync):
	_sh_ = True
<<<<<<< HEAD
	_aal = False
	_dbg = False
=======
	_aal = None
	_dbg = False
	_mode = 'sync'
	svn = SubVersion()
>>>>>>> 3cabfc8e133237046ff5fb204d59ccde90c8af7d
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
<<<<<<< HEAD
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
=======
			setattr(self, key, val)
>>>>>>> 3cabfc8e133237046ff5fb204d59ccde90c8af7d
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
		self._dbg = val

<<<<<<< HEAD
	def sync(self, repo, *branchs, mode='sync', syncall=None):
		if self.dbg:
			print('%s'%self.sync)
		if os.path.exists(repo):
			os.chdir(repo)
			if (os.path.isdir('%s/.git'%repo) or \
                  os.path.isfile('%s/.gitmodules'%repo) or \
                  os.path.isfile('%s/.git'%repo)):
				self.gitsync(branchs, mode, syncall)
			elif os.path.isdir(repo+'/.svn'):
				# on svn repositories i can only sync remote to local
				self.call('svn up')
			# i lack support of any other versioning too till now



=======
	def sync(self, repotypes):
		if self.dbg:
			print(self.sync)
		self.syncgits(*[r for (r, t) in repotypes.items() if t == 'git'])
		svns = [r for (r, t) in repotypes.items() if t == 'svn']
		if svns:
			for svnrpo in svns:
				self.svn.svnupdate(svnrepo)
>>>>>>> 3cabfc8e133237046ff5fb204d59ccde90c8af7d



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
