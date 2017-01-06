#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import sys
from os import chdir
from os.path import basename, dirname, isfile

# local relative imports
from colortext import blu, yel, bgre, tabd, error
from repo.git import GitRepo


class GitSync(GitRepo):
	_sh_ = True
	_dbg = False
	syncmode = 'sync' # commit|push|pull
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(GitSync.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	def _gitsubmods(self, repos):
		if self.dbg:
			print(bgre(self._gitsubmods))
		def __gitmods(gitmodfile):
			with open(gitmodfile, 'r') as gmf:
				modlines = gmf.readlines()
			return [l.split('=')[1].strip() for l in modlines if 'path =' in l]
		def __modpaths(gitdir):
			modfile = '%s/.gitmodules'%gitdir
			if isfile(modfile):
				return ['%s/%s'%(gitdir, m) for m in __gitmods(modfile)]
		for repo in repos:
			mods = __modpaths(repo)
			if mods:
				repos = self._gitsubmods(mods) + list(repos)
		return repos

	def gitsync(self, branch=None):
		if self.dbg:
			print(bgre(self.gitsync))
		branch = branch if branch else self._head()
		if branch != self._head(): self.checkout(branch)
		self.pull()
		status, ahead, behind = self.gitstatus()
		if not status and not ahead and not behind: return
		if ahead: self.push(branch)
		if status != {}:
			self.add()
			self.commit(status)
		_, ahead, _ = self.gitstatus()
		if ahead: self.push(branch)
		if status:
			return {branch: status}

	def giter(self, repos, syncall=None):
		if self.dbg:
			print(bgre('%s\n  repos = %s\n  syncall = %s'%(
                self.giter, repos, syncall)))
		for repo in self._gitsubmods(repos):
			try:
				chdir(repo)
			except FileNotFoundError:
				error('path', repo, 'does not exist and has been omitted')
				continue
			print(blu('syncing'), '%s%s'%(yel(repo), blu('...')))
			branchstats = {}
			head = self._head()
			branchs = [head]
			if syncall:
				branchs = [
                    b for b in self._heads() if not b in ('master', head)]
			for branch in branchs:
				stats = self.gitsync(branch)
				if not stats:
					continue
				branchstats.update(stats)
			if self.dbg and branchstats:
				print(bgre('{%s: %s}'%(repo, branchstats)))
			if branchstats:
				yield {repo: branchstats}



if __name__ == '__main__':
	exit(1)
