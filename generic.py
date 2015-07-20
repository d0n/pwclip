#!/usr/bin/env python3
"""repo common functions module"""
# global imports
from os import listdir as _listdir, chdir as _chdir
from os.path import exists as _exists, isdir as _isdir

# local relative imports
from lib.colortext import blu, yel
#from .subversion import SubVersion

from .git import GitSync

# default vars
__version__ = '0.1'

class RepoSync(GitSync):
	_sh_ = True
	_aal = None
	_dbg = False
	_mode = 'sync'
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
		self._dbg = val

	def sync(self, repotypes):
		if self.dbg:
			print(self.sync)
		gits = [r for (r, t) in repotypes.items() if t == 'git']
		svns = [r for (r, t) in repotypes.items() if t == 'svn']
		if gits:
			for branchstat in self.syncgits(*gits):
				print(branchstat)
		if svns:
			for svnrpo in svns:
				_chdir(svnrpo)
				if self.call('%s update'%which('svn')) != 0:
					error('svn command exited with non zero status')




if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
