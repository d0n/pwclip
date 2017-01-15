#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
from os.path import isfile
import sys

# local relative imports
from executor import Command
from system import absrelpath, which
from colortext import blu, yel, tabd, bgre, error

# default vars
__version__ = '0.1'

class GitRepo(Command):
	"""
	git repo class derives the Command class to provide wrapping methods using
	the git binary found on the system
	"""
	# external attributes
	sh_ = True
	dbg = None
	vrb = None
	lwd = None
	gitremote = ''
	_gitdir = None
	_gitbin = which('git')
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '_%s'%(key)):
				setattr(self, '_%s'%(key), val)
		if not self.gitbin:
			raise RuntimeError('could not find git binary in $PATH')
		if self.dbg:
			print(bgre(GitRepo.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

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

	@property               # gitbin <str>
	def gitbin(self):
		return self._gitbin

	@staticmethod
	def __gitdir_(repodir):
		def __file(git):
			with open(git, 'r') as gitf:
				return os.path.abspath(gitf.read().split('gitdir:')[1].strip())
		repodir = repodir.rstrip('/')
		gitdir = '%s/.git'%(repodir)
		if os.path.isfile(gitdir):
			return __file(gitdir)
		else:
			c = len(repodir.split('/'))
			while c > 0:
				if os.path.isdir(gitdir):
					return gitdir
				gitdir = '%s/.git'%'/'.join(d for d in repodir.split('/')[:c])
				c-=1
		raise FileNotFoundError('no .git directory present in %s'%repodir)

	def _fetch_(self, fetchall=False):
		if self.dbg:
			print(bgre(self._fetch_))
		cmd = '%s fetch'%self.gitbin
		if fetchall:
			cmd = '%s --all'%cmd
		if self.erno(cmd) == 0:
			return True

	def _head(self):
		if self.dbg:
			print(bgre(self._head))
		#print(self.gitdir)
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
		return [h for h in heads if h != head] + [head]

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

	def pull(self, branch=None, origin='origin', verbose=False):
		if self.dbg:
			print(bgre(self.pull))
		branch = branch if branch else self._head()
		o, e, n = self.oerc('%s pull %s %s'%(self.gitbin, origin, branch))
		o, e = o.strip(), e.strip()
		if o and o != 'Already up-to-date.':
			print(o)
		elif verbose and e:
			print('%s\n%s'%(o, e))
		return n

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

	def clone(self, remote, target, branch='master'):
		if self.dbg:
			print(bgre(self.cloe))
		command = '%s clone -b %s %s %s'%(self.gitbin, branch, remote, target)
		return self.call(command)

	def commit(self, message):
		if self.dbg:
			print(bgre(self.commit))
		command = '%s commit -a -m "%s"' %(self.gitbin, message)
		return int(self.call(command))

	def commitstamp(self, rpofile):
		if self.dbg:
			print(bgre(self.commitstamp))
		rpofile = absrelpath(rpofile)
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

	def gitlog(self, *args):
		if self.dbg:
			print(bgre(self.gitlog))
		logs, ermsg, ernum = self.oerc(
            '%s log'%self.gitbin)
		return logs.split('\n')

	def gitsubmods(self, repos):
		if self.dbg:
			print(bgre(self.gitsubmods))
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
				repos = self.gitsubmods(mods) + list(repos)
		return repos

	def gittreepull(self, prefix):
		out, err, eno = self.oerc('%s subtree pull -P %s'%(
            self.gitbin, prefix))

	def gittreepush(self, prefix):
		out, err, eno = self.oerc('%s subtree push -P %s'%(
            self.gitbin, prefix))

	def gitsubtrees(self):
		if self.dbg:
			print(bgre(self.gitsubtrees))
		strees = []
		trees = list(set([
            l.split(': ')[1] for l in self.gitlog() if 'git-subtree-dir' in l
            ]))
		if trees:
			lens = list(set([len(t.split('/')) for t in trees]))
			for i in reversed(lens):
				for tree in sorted(trees):
					if len(tree.split('/')) == i:
						if not tree in strees: strees.append(tree)
		return strees

	def gitstatus(self):
		if self.dbg:
			print(bgre(self.gitstatus))
		stats, ermsg, ernum = self.oerc(
            '%s status -b --porcelain'%self.gitbin)
		if ermsg or ernum != 0:
			error(
                'command', 'git status',
                'exited with errorcode',
                '%d'%ernum, 'and message:\n',
                '%s'%ermsg)
		stats = stats.split('\n')
		ablines = [l for l in stats if l.startswith('##')]
		anum, bnum = 0, 0
		for abline in ablines:
			if not '[' in abline or not ']' in abline:
				continue
			__ahbe = abline.split('[')[-1].strip(']').split(',')
			if len(__ahbe) > 1:
				anum, bnum = __ahbe[0].strip().split(' ')[1], \
                             __ahbe[1].strip().split(' ')[1]
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
                msg, blu('%s%s'%(typ[0].upper(),
                typ[1:])), ', '.join(yel(f) for f in stats[typ]))
		msg = msg.strip(', ')
		msg = '%s }'%(msg)
		return msg


if __name__ == '__main__':
	exit(1)
