#!/usr/bin/env python3
"""repo common functions module"""
# global imports
from os import listdir as _listdir, chdir as _chdir
from os.path import exists as _exists, isdir as _isdir

# local relative imports
from colortext import blu, yel, bgre, tabd, error
from system import which
from repo.git import GitSync

# default vars
__version__ = '0.1'

class RepoSync(GitSync):
	_sh_ = True
	_dbg = False
	abr = False
	syncmode = 'sync'
	svnuser = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '_%s'%(arg)):
				setattr(self, '_%s'%(arg), True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '_%s'%(key)):
				setattr(self, '_%s'%(key), val)
		if self.dbg:
			print(bgre(RepoSync.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		GitSync.__init__(self, *args, **kwargs)

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	def rposync(self, repotypes, syncmode=None, syncall=None):
		if self.dbg:
			print(bgre('%s\n  repotypes = %s\n  syncmode = %s'%(
                self.rposync, repotypes, syncmode)))
		syncmode = syncmode if syncmode else self.syncmode
		syncall = syncall if syncall else self.abr
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
				out, err, eno = self.oerc(
                    '%s%s update'%(which('svn'), svnopts))
				if eno != 0:
					error(err)
				if out:
					out.translate(('\\n', '>> '))
					print(out)
				repostats.append({repo: out})
		if repostats:
			return repostats



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
