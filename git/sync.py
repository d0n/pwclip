#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
from os import chdir as _chdir
from os.path import isfile as _isfile, exists as _exists, basename as _basename
import sys

# local relative imports
from lib.executor import Command
from lib.system import realpaths, which
from lib.colortext import blu, yel, bgre, error

from .repo import GitRepo

class GitSync(GitRepo):
	# external
	_sh_ = True
	# internal
	_aal = False
	_dbg = False
	_mode = 'sync'

	@property                # aal <bool>
	def aal(self):
		return self._aal
	@aal.setter
	def aal(self, val):
		self._aal = True if val else False

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	@property                # mode <str>
	def mode(self):
		return self._mode
	@mode.setter
	def mode(self, val):
		self._mode = val if isinstance(val, str) else self._mode

	def _gitsubmods(self, repos):
		if self.dbg:
			print(bgre(self._gitsubmods))
		def __gitmods(gitmodfile):
			with open(gitmodfile, 'r') as gmf:
				modlines = gmf.readlines()
			return [l.split('=')[1].strip() for l in modlines if 'path =' in l]
		def __modpaths(gitdir):
			modfile = '%s/.gitmodules'%gitdir
			if _isfile(modfile):
				return ['%s/%s'%(gitdir, m) for m in __gitmods(modfile)]
		for repo in repos:
			mods = __modpaths(repo)
			if mods:
				repos = self._gitsubmods(mods) + list(repos)
		return repos

	def gitsync(self, branch, mode=''):
		if self.dbg:
			print(bgre('%s\n  branchs = %s\n  mode = %s'%(
                self.gitsync, branch, mode)))
		mode = mode if mode else self.mode
		status = self.gitstatus()
		if not status:
			return
		print(status)
		isahead, isbehind = False, False
		if 'A' in status.keys():
			isahead = True
			del status['A']
		if 'B' in status.keys():
			isbehind = True 
			del statsu['B']
		if isahead:
			self.pull(branch)
		self.add()
		self.commit(status)
		if isbehind:
			self.push(branch)
		return {branch: status}

	def itergits(self, repos, mode='', syncall=None):
		if self.dbg:
			print(bgre('%s\n  repos = %s\n  mode = %s\n  syncall = %s'%(
                self.itergits, repos, mode, syncall)))
		mode = mode if mode else self.mode
		syncall = syncall if syncall else self._aal
		for repo in self._gitsubmods(repos):
			_chdir(repo)
			if not _exists(repo):
				error('path %s does not exist and has been omitted'%repo)
				continue
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			branchs = self._heads() if syncall else [self._head()]
			syncstats = {}
			for branch in branchs:
				stats = self.gitsync(branch, mode)
				if not stats:
					continue
				syncstats.update(stats)
			if syncstats:
				yield {_basename(repo): syncstats}

if __name__ == '__main__':
	exit(1)
