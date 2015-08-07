#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
from os import chdir as _chdir
from os.path import isfile as _isfile, exists as _exists
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
	_abr = False
	_dbg = False
	_mode = 'sync'

	@property                # abr <bool>
	def abr(self):
		return self._abr
	@abr.setter
	def abr(self, val):
		self._abr = val if isinstance(val, bool) else self._abr

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if isinstance(val, bool) else self._dbg

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
		if status:
			if status['isbehind']:
				self.pull()
			self.add()
			self.commit(status)
			if status['isahead']:
				self.push()
			return {branch: status}

	def itergits(self, repos, mode='', syncall=None):
		if self.dbg:
			print(bgre('%s\n  repos = %s\n  mode = %s\n  syncall = %s'%(
                self.itergits, repos, mode, syncall)))
		mode = mode if mode else self.mode
		for repo in self._gitsubmods(repos):
			_chdir(repo)
			if not _exists(repo):
				error('path %s does not exist and has been omitted'%repo)
				continue
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			branchs = [self._head()]
			if syncall or self.abr:
				branchs = self._heads()
			syncstats = {}
			for branch in branchs:
				stats = self.gitsync(branch, mode)
				if not stats:
					continue
				syncstats[branch] = stats
			yield {repo: syncstats}

if __name__ == '__main__':
	exit(1)
