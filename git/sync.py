#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import sys
from os import chdir, getcwd
from os.path import basename, dirname, isfile

# local relative imports
from colortext import blu, yel, bgre, tabd, error
from repo.git import GitRepo


class GitSync(GitRepo):
	sh_ = True
	dbg = False
	abr = False
	remote = ''
	rpodir = ''
	subtree = ''
	syncmodes = ['sync'] # commit|push|pull
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(GitSync.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		GitRepo.__init__(self, *args, **kwargs)

	def gitsync(self, branch=None):
		if self.dbg:
			print(bgre(self.gitsync))
		branch = branch if branch else self._head()
		if branch != self._head(): self.checkout(branch)
		if [m for m in self.syncmodes if m in ('sync', 'pull')]:
			self.pull()
		status, ahead, behind = self.gitstatus()
		if not status and not ahead and not behind: return
		if [m for m in self.syncmodes if m in ('sync', 'push')]:
			if ahead: self.push(branch)
		if [m for m in self.syncmodes if m in ('sync', 'commit')]:
			if status:
				self.add()
				self.commit(status)
		_, ahead, _ = self.gitstatus()
		if [m for m in self.syncmodes if m in ('sync', 'push')]:
			if ahead: self.push(branch)
		if status:
			return {branch: status}

	def treesync(self):
		if self.dbg:
			print(bgre(self.treesync))
		if not self.remote or not self.rpodir or not self.subtree:
			raise AttributeError(
                'at least on mandatory attribute was not assigned ' \
                'remote: %s, rpodir: %s, subtree: %s'%(
                    self.remote, self.rpodir, self.subtree))
		stats = {}
		trees = self.gitsubtrees()
		if trees and self.gitremote:
			print(blu('syncing subtrees: %s'%(yel(getcwd()))))
			for tree in trees:
				print(' ', yel(tree))
				if [m for m in self.syncmodes if m in ('sync', 'pull')]:
					self.gittreepull(tree)
				if [m for m in self.syncmodes if m in ('sync', 'push')]:
					self.gittreepush(tree)

	def giter(self, repos, syncall=None):
		if self.dbg:
			print(bgre('%s\n  repos = %s\n  syncall = %s'%(
                self.giter, repos, syncall)))
		syncall = syncall if syncall else self.abr
		for repo in self.gitsubmods(repos):
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
				branchs = [b for b in self._heads() if not b == head] + [head]
			for branch in branchs:
				stats = self.gitsync(branch)
				if stats:
					branchstats[branch] = stats
			if self.dbg and branchstats:
				print(bgre('{%s: %s}'%(repo, branchstats)))
			treestats = self.treesync()
			if branchstats:
				yield {repo: branchstats}

if __name__ == '__main__':
	exit(1)
