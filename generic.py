#!/usr/bin/env python3
"""repo common functions module"""
# global imports
from os import listdir as _listdir, chdir as _chdir
from os.path import exists as _exists, isdir as _isdir

# local relative imports
from colortext import blu, yel, bgre
#from .subversion import SubVersion
from system import which
from repo.git import GitSync

# default vars
__version__ = '0.1'

class RepoSync(GitSync):
	_sh_ = True
	_aal = False
	_dbg = False
	_mode = 'sync'
	_svnuser = ''
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
			print(bgre('%s\n%s\n\n%s\n%s\n'%(
                RepoSync.__mro__,
               '\n'.join('  %s%s=\t%s'%(
                    k, ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(RepoSync.__dict__.items())),
                RepoSync.__init__,
                '\n'.join('  %s%s=\t%s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items())))))

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	def rposync(self, repotypes, mode=None, syncall=None):
		if self.dbg:
			print(bgre('%s\n  repotypes = %s\n  mode = %s'%(
                self.rposync, repotypes, mode)))
		mode = mode if mode else self.mode
		syncall = syncall if syncall else self._aal
		repostats = []
		if 'git' in repotypes.keys():
			for rbstat in self.giter(repotypes['git'], syncall):
				repostats.append(rbstat)
		if 'svn' in repotypes.keys():
			svnopts = ' --username=%s'%self._svnuser if self._svnuser else ''
			stats = {}
			for repo in sorted(repotypes['svn']):
				_chdir(repo)
				print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
				out = self.stdo('%s%s update'%(which('svn'), svnopts))
				repostats.append({repo: out})
		if repostats:
			return repostats



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
