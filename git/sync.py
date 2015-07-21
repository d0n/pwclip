#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
from os.path import isfile as _isfile
import sys

# local relative imports
from lib.misc import which
from lib.executor import Command
from lib.system import realpaths
from lib.colortext import blu, yel, error

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
			print(self.gitsync)
		mode = mode if mode else self.mode
		branchstats = {}
		for branch in branchs:
			status = self.gitstatus()
			if status:
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
			print(self.itergits)
		mode = mode if mode else self.mode
		for repo in self._gitsubmods(repos):
			if not os.path.exists(repo):
				error('path %s does not exist and has been omitted'%repo)
				continue
			os.chdir(repo)
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			if not os.path.exists(repo):
				continue
			if not branchs:
				branchs = [self._head()]
				if self.abr:
					branchs = self._heads()
			if checkout:
				branchs = [b for b in branchs if b != checkout] + [checkout]
			yield repo, self.gitsync(branchs, mode)

if __name__ == '__main__':
	exit(1)
