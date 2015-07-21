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
from lib.colortext import blu, yel

from .repo import GitRepo

class GitSync(GitRepo):
	# external
	_sh_ = True
	# internal
	_dbg = False
	_abr = False
	_mode = ''
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if isinstance(val, bool) else self._dbg

	@property                # aal <bool>
	def aal(self):
		return self._aal
	@aal.setter
	def aal(self, val):
		self._aal = val if isinstance(val, bool) else self._aal

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

	def gitsync(branchs, mode, recurse=True):
		

	def itergits(
          self, *repos, branchs=[], mode='', allbranchs=False, checkout=None):
		if self.dbg:
			print(self.syncgits)
		_all = syncall if syncall else self.aal
		mode = mode if mode else self.mode
		repobranchstats = {}
		for repo in self._gitsubmods(repos):
			if not os.path.exists(repo):
				continue
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			os.chdir(repo)
			_head = checkout if checkout else self._head()
			branchs = [_head]
			if _all:
				branchs = [h for h in self._heads() if h != _head] + [_head]
			branchstats = {}
			for branch in branchs:
				if not branch == self._head():
					self.checkout(branch)
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
				repobranchstats[repo] = branchstats
		if repobranchstats != {}:
			return repobranchstats

if __name__ == '__main__':
	exit(1)
