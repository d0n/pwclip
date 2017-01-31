#!/usr/bin/env python3
"""repo common functions module"""
# global imports
from os import chdir

# local relative imports
from colortext import blu, yel, bgre, tabd, error
from system import which
from repo.git import GitSync

# default vars
__version__ = '0.1'

class RepoSync(GitSync):
	sh_ = True
	dbg = None
	abr = None
	tsy = None
	svnuser = ''
	syncmodes = ['sync']
	gitkwargs = {}
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(RepoSync.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		if 'gitkwargs' in kwargs.keys():
			self.gitkwargs = kwargs['gitkwargs']
		GitSync.__init__(self, *args, **self.gitkwargs)

	def rposync(self, repotypes, syncall=None):
		if self.dbg:
			print(bgre('%s\n  repotypes = %s\n'%(self.rposync, repotypes)))
		syncall = syncall if syncall else self.abr
		repostats = []
		if 'git' in repotypes.keys():
			rbstat = self.giter(repotypes['git'], syncall)
			if rbstat:
				repostats.append(rbstat)
			if self.tsy:
				rbstat['treesync'] = self.treesync()
		if 'svn' in repotypes.keys():
			svnopts = ' --username=%s'%self.svnuser if self.svnuser else ''
			stats = {}
			for repo in sorted(repotypes['svn']):
				chdir(repo)
				print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
				out, err, eno = self.oerc(
                    '%s%s update'%(which('svn'), svnopts))
				if eno != 0:
					error(err)
				if out:
					out.translate(('\\n', '>> '))
					print(out.strip())
				repostats.append({repo: out})
		if repostats:
			return repostats



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
