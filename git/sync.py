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
			print(self._gitsubmods)
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

	def gitsync(self, branchs=['master'], mode=''):
		if self.dbg:
			print(bgre('%s %s %s'%(self.gitsync, branchs, mode)))
		mode = mode if mode else self.mode
		branchstats = {}
		for branch in branchs:
			status = self.gitstatus()
			if status:
				print(status)
				if mode in ('sync', 'push'):
					if status:
						self.add()
						self.commit(status)
						branchstats[branch] = status
				if mode in ('sync', 'pull'):
					self.pull()
				if mode in ('sync', 'push'):
					self.push()
		if branchstats != {}:
			return branchstats

	def itergits(self, repos, branchs=[], mode='', checkout=None):
		if self.dbg:
			print(bgre(self.itergits))
		mode = mode if mode else self.mode
		for repo in self._gitsubmods(repos):
			if not _exists(repo):
				error('path %s does not exist and has been omitted'%repo)
				continue
			_chdir(repo)
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			if not branchs:
				branchs = [self._head()]
				if self.abr:
					branchs = self._heads()
			if checkout:
				branchs = [b for b in branchs if b != checkout] + [checkout]
			yield repo, self.gitsync(branchs, mode)

if __name__ == '__main__':
	exit(1)
