#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
from os.path import isfile as _isfile
import sys

# local relative imports
from lib.executor import Command
from lib.system import realpaths, which
from lib.colortext import blu, yel, bgre

# default vars
__version__ = '0.1'

"""
def _headref_(self):
	if self.dbg:
		print(bgre(self._headref_))
	hrefile = '%s/refs/heads/%s'%(self.gitdir, self._head())
	if os.path.isfile(hrefile):
		with open(hrefile, 'r') as f:
			return f.read().split(' ')[0].strip()

def _remoteref_(self):
	if self.dbg:
		print(bgre(self._remoteref_))
	remref = '%s/refs/remotes/origin/%s'%(self.gitdir, self._head())
	if os.path.isfile(remref):
		with open(remref, 'r') as f:
			return f.read().strip()

def _logrefs_(self):
	rlog = '%s/logs/refs/heads/%s'%(self.gitdir, self._head())
	with open('%s/logs/refs/heads/%s'%(
		  self.gitdir, self._head())) as log:
		return [l.split()[:2] for l in  log.readlines()]
"""

class GitRepo(Command):
	# Command attribute
	_sh_ = True
	# GitRepo attributes
	_dbg = False
	_lwd = None
	_gitdir = None
	_gitbin = which('git')
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(GitRepo.__mro__))
			for (key, val) in self.__dict__.items():
				print(bgre(key, '=', val))
		if not self.gitbin:
			raise RuntimeError('could not find git binary in $PATH')

	# rw propereties
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	@property                # lwd <str>
	def lwd(self):
		return self._lwd
	@lwd.setter
	def lwd(self, val):
		self._lwd = os.path.abspath(val)

	@property                # gitdir <str>
	def gitdir(self):
		cwd = os.getcwd()
		if not self._gitdir or cwd != self.lwd:
			return self.__gitdir_(cwd)
		return self._gitdir
	@gitdir.setter
	def gitdir(self, val):
		if os.path.isdir(val):
			self._gitdir = self.__gitdir_(val)
		else:
			raise ValueError('directory %s does not exist'%val)

	# ro properties
	@property               # gitbin <str>
	def gitbin(self):
		return self._gitbin

	@staticmethod
	def __gitdir_(repodir):
		gitdir = '%s/.git'%(repodir)
		if os.path.isfile(gitdir):
			with open(gitdir, 'r') as gitf:
				return '%s/%s'%(
                    repodir, gitf.read().split('gitdir:')[1].strip())
		else:
			c = len(repodir.split('/'))
			while c != 0:
				if not os.path.isdir(gitdir):
					gitdir = '%s/%s'%(
                        gitdir, '/'.join(
                            d for d in repodir.split('/')[:c])+'/.git')
				c-=1
			return gitdir

	def _fetch(self, fetchall=True):
		cmd = '%s fetch'%self.gitbin
		if fetchall:
			cmd = '%s --all'%cmd
		return self.call(cmd)

	def _head(self):
		if self.dbg:
			print(bgre(self._head))
		with open('%s/HEAD'%(self.gitdir), 'r') as f:
			return f.read().split('/')[-1].strip()

	def _heads(self):
		if self.dbg:
			print(bgre(self._heads))
		if not os.path.exists('%s/refs/heads'%(self.gitdir)):
			errmsg = 'no basedir was set and current one is no git repo %s'%(
                self.gitdir)
			raise RuntimeError(errmsg)
		head, heads = self._head(), os.listdir('%s/refs/heads'%(self.gitdir))
		return [head] + [h for h in heads if h != head]

	def _remotes(self):
		if self.dbg:
			print(bgre(self._remotes))
		return [rem for rem in os.listdir(
	        '%s/refs/remotes/origin/'%(self.gitdir)) if rem != 'HEAD']

	def checkout(self, branch, *files):
		if self.dbg:
			print(bgre(self.checkout))
		heads = self._heads()
		if files:
			command = '%s checkout %s %s'%(
                self.gitbin, branch,
                ' '.join(f for f in files if files and f))
		elif not branch in heads:
			command = '%s checkout -b %s'%(self.gitbin, branch)
		else:
			command = '%s checkout %s'%(self.gitbin, branch)
		return self.erno(command)

	def pull(self, branch=None, origin='origin'):
		if self.dbg:
			print(bgre(self.pull))
		branch = branch if branch else self._head()
		command = '%s pull %s %s' %(self.gitbin, origin, branch)
		return int(self.call(command))

	def push(self, remote=None, origin='origin', setup=None):
		if self.dbg:
			print(bgre(self.push))
		remote = remote if remote else self._head()
		command = '%s push %s %s'%(self.gitbin, origin, remote)
		if setup or remote not in self._remotes():
			command = '%s push --set-upstream %s %s'%(
                self.gitbin, origin, remote)
		return int(self.call(command))

	def add(self, *files):
		if self.dbg:
			print(bgre(self.add))
		command = '%s add -A'%(self.gitbin)
		if files:
			command = '%s add %s'%(self.gitbin, ' '.join(f for f in files))
		return int(self.call(command))

	def commit(self, message):
		if self.dbg:
			print(bgre(self.commit))
		command = '%s commit -a -m "%s"' %(self.gitbin, message)
		return int(self.call(command))

	def commitstamp(self, rpofile):
		if self.dbg:
			print(bgre(self.commitstamp))
		rpofile = realpaths(rpofile)
		stamp = self.stdo('%s log -1 --format=%%at %s'%(self.gitbin, rpofile))
		if stamp:
			stamp = stamp.strip()
			return int(stamp)

	def show(self, *args, **kwargs):
		if self.dbg:
			print(bgre(self.show))
		cmd = '%s show' %(self.gitbin)
		if 'commitstamp' in args:
			cmd = '%s show -s --format=%%at' %(self.gitbin)
		return self.stdo(cmd).strip()

	def gitstatus(self):
		if self.dbg:
			print(bgre(self.gitstatus))
		stats = self.stdx('%s status -b --porcelain'%self.gitbin).split('\n')
		ablines = [l for l in stats if l.startswith('##')]
		anum, bnum = 0, 0
		for abline in ablines:
			if not '[' in abline or not ']' in abline:
				continue
			__ahbe = abline.split('[')[-1].strip(']').split(',')
			if len(__ahbe) > 1:
				anum, bnum = __ahbe[0].strip().split(' ')[1], __ahbe[1].strip().split(' ')[1]
			elif 'ahead' in __ahbe[0]:
				anum = __ahbe[0].split(' ')[1].strip()
			elif 'behind' in __ahbe[0]:
				bnum = __ahbe[0].split(' ')[1].strip()
		status = {}
		adds = []
		mods = []
		dels = []
		rens = []
		for line in stats:
			if not line:
				continue
			if line.split()[0] in ('A', '??', '?'):
				adds.append(line.split()[1])
			elif line.split()[0] == 'D':
				dels.append(line.split()[1])
			elif line.split()[0] in ('M', 'MM'):
				mods.append(line.split()[1])
			elif line.split()[0] == 'R':
				rens.append(line.split()[1:])
		if mods != []:
			status['modified'] = mods
		if dels != []:
			status['deleted'] = dels
		if adds != []:
			status['added'] = adds
		if rens != []:
			status['renamed'] = rens
		return status, int(anum), int(bnum)

	def genmessage(self, stats=None):
		if self.dbg:
			print(bgre(self.genmessage))
		if not stats:
			stats = self.gitstatus()
			if not stats:
				return
		msg = '{ '
		for typ in stats:
			msg = '%s%s: [%s], '%(
                msg, blu('%s%s'%(typ[0].upper(), typ[1:])),
                ', '.join(yel(f) for f in stats[typ]))
		msg = msg.strip(', ')
		msg = '%s }'%(msg)
		return msg


if __name__ == '__main__':
	exit(1)
