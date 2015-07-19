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

# default vars
__version__ = '0.1'

class GitRepo(Command):
	# Command class attribute
	_sh_ = True
	# own attributes
	_dbg = False
	_gitdir = ''
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
			print(GitRepo.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
		if not self.gitbin:
			raise RuntimeError('could not find git binary in $PATH')

	# rw propereties
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	@property                # gitdir <str>
	def gitdir(self):
		return self._gitdir if self._gitdir else self.__gitdir(os.getcwd())
	@gitdir.setter
	def gitdir(self, val):
		if os.path.isdir(val):
			self._gitdir = self.__gitdir(val)
		else:
			raise ValueError(
                'cannot set %s as directory while it does not exist'%val)

	# ro properties
	@property               # gitbin <str>
	def gitbin(self):
		return self._gitbin

	@staticmethod
	def __gitdir(repodir):
		gitdir = '%s/.git'%(repodir)
		c = len(repodir.split('/'))
		while c != 0:
			if os.path.isdir(gitdir):
				return gitdir
			gitdir = '/'.join(d for d in repodir.split('/')[:c])+'/.git'
			c-=1

	def _fetch_(self, fetchall=None):
		if self.dbg:
			print(self._fetch)
		command = '%s fetch'%self.gitbin
		if fetchall:
			command = '%s fetch --all'%self.gitbin
		if self.erno(command) == 0:
			return True

	def _fetchref_(self):
		if self.dbg:
			print(self._fetchref_)
		fetchead = '%s/FETCH_HEAD'%self.gitdir
		if os.path.isfile(fetchead):
			with open(fetchead, 'r') as f:
				return f.read().split('\t')[0].strip()

	def _headref_(self):
		if self.dbg:
			print(self._headref_)
		hrefile = '%s/refs/heads/%s'%(self.gitdir, self._head())
		if os.path.isfile(hrefile):
			with open(hrefile, 'r') as f:
				return f.read().split(' ')[0].strip()

	def _heads(self):
		if self.dbg:
			print(self._heads)
		if not os.path.exists('%s/refs/heads'%(self.gitdir)):
			errmsg = 'no basedir was set and current one is no git repo %s'%(
                self.gitdir)
			raise RuntimeError(errmsg)
		return os.listdir('%s/refs/heads'%(self.gitdir))

	def _head(self):
		if self.dbg:
			print(self._head)
		with open('%s/HEAD'%(self.gitdir), 'r') as f:
			return f.read().split('/')[-1].strip()

	def _remoteref(self):
		if self.dbg:
			print(self._remoteref)
		self._fetch_(fetchall=True)
		gitdir = self.gitdir
		remref = '%s/refs/remotes/origin/%s'%(gitdir, self._head())
		if not os.path.isfile(remref):
			remref = '%s/refs/remotes/origin/HEAD'%(gitdir)
		with open(remref, 'r') as f:
			return f.read().strip()

	def _remotes(self):
		if self.dbg:
			print(self._remotes)
		return [rem for rem in os.listdir(
	        '%s/refs/remotes/origin/'%(self.gitdir)) if rem != 'HEAD']

	def _isbehind(self):
		if self.dbg:
			print(self._isbehind)
		if self._remoteref() != self._headref_():
			return True

	def _isahead(self):
		if self.dbg:
			print(self._isahead)
		if self._headref_() != self._fetchref_():
			return True

	def checkout(self, branch, *files):
		if self.dbg:
			print(self.checkout)
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

	def pull(self, origin='origin'):
		if self.dbg:
			print(self.pull)
		command = '%s pull %s' %(self.gitbin, origin)
		out = self.stdx(command)
		if out:
			return out

	def push(self, remote=None, origin='origin', setup=None):
		if self.dbg:
			print(self.push)
		if not remote:
			remote = self._head()
		command = '%s push %s %s'%(self.gitbin, origin, remote)
		if setup or remote not in self._remotes():
			command = '%s push --set-upstream %s %s'%(
                self.gitbin, origin, remote)
		return int(self.call(command))

	def add(self, *files):
		if self.dbg:
			print(self.add)
		command = '%s add -A'%(self.gitbin)
		if files:
			command = '%s add %s'%(self.gitbin, ' '.join(f for f in files))
		return int(self.call(command))

	def commit(self, message):
		if self.dbg:
			print(self.commit)
		command = '%s commit -a -m "%s"' %(self.gitbin, message)
		return int(self.call(command))

	def commitstamp(self, rpofile):
		if self.dbg:
			print(self.commitstamp)
		rpofile = realpaths(rpofile)
		stamp = self.stdo('%s log -1 --format=%%at %s'%(self.gitbin, rpofile))
		if stamp:
			stamp = stamp.strip()
			return int(stamp)

	def show(self, *args, **kwargs):
		if self.dbg:
			print(self.show)
		cmd = '%s show' %(self.gitbin)
		if 'commitstamp' in args:
			cmd = '%s show -s --format=%%at' %(self.gitbin)
		return self.stdo(cmd).strip()

	def gitstatus(self, mode='--porcelain'):
		if self.dbg:
			print(self.gitstatus)
		out = self.stdx('%s status %s'%(self.gitbin, mode))
		if not out or mode != '--porcelain':
			return out
		stats = {}
		adds = []
		mods = []
		dels = []
		rens = []
		for line in out.split('\n'):
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
			stats['modified'] = mods
		if dels != []:
			stats['deleted'] = dels
		if adds != []:
			stats['added'] = adds
		if rens != []:
			stats['renamed'] = rens
		if stats != {}:
			return stats

	def genmessage(self, stats=None):
		if self.dbg:
			print(self.genmessage)
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



class GitSync(GitRepo):
	# external
	_sh_ = True
	# internal
	_dbg = False
	_aal = False
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

	def syncgits(self, *repos, mode=None, syncall=None, checkout=None):
		if self.dbg:
			print(self.syncgits)
		_all = syncall if syncall else self.aal
		mode = mode if mode else self.mode
		for repo in self._gitsubmods(repos):
			if not os.path.exists(repo):
				continue
			os.chdir(repo)
			_head = checkout if checkout else self._head()
			branchs = [_head]
			if _all:
				branchs = [h for h in self._heads() if h != _head] + [_head]
			branchstats = {}
			for branch in branchs:
				print(blu('syncing branch'), yel(branch), blu('in'), yel(repo))
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
			return branchstats

class GitClone(GitRepo):
	user = os.getenv('USER')
	remote = None
	repodir = None
	dbg = None
	def __init__(self, *args, **kwargs):
		if 'debug' in kwargs.keys():
			self.dbg = kwargs['debug']
		if 'remote' in kwargs.keys():
			self.remote = kwargs['remote']
		if 'user' in kwargs.keys():
			self.user = kwargs['user']
		if 'rpodir' in kwargs.keys():
			self.rpodir = kwargs['rpodir']
		if self.dbg:
			print(GitClone.__mro__)
			print('user', self.user)
			print('remote', self.remote)
			print('repodir', self.rpodir)
			print()

	def clone(self, repo, target=None):
		if self.repodir:
			repo = self.repodir+'/'+repo
		remote = self.user+'@'+self.remote+':'+repo+'.git'
		command = git+' clone '+remote
		if target:
			if not os.path.isdir('/'.join(d for d in target.split('/')[:-1])):
				os.makedirs('/'.join(d for d in target.split('/')[:-1]))
			command = command+' '+target
		if int(self.call(command)) == 0:
			return True












if __name__ == '__main__':
	"""
	# by default my modules print all classes/definitions they own
	for func in dir(sys.modules[__name__]):
		if not '-v' in sys.argv:
			if str(func).startswith('__') or func == 'func':
				continue
		print(func)
		if func in sys.argv:
			print(dir(func))
			continue
	print()
	"""
	#git = GitClone(**{'debug':True, 'remote':'bigbox.janeiskla.de', 'repodir':'rpo'})
	#git.clone('bin', 'rpo/bin')
	#repo = RepoSync() #**{'repo':'/home/d0n/rpo/housewife'})
	#print(repo._gitdir())
	#print(int(os.stat('home/USER/.bash_tail').st_mtime))
	#print(repo.commitstamp('home/USER/.bash_tail'))
	git = GitRepo(**{'repodir': '/home/d0n/cfg'})
	print(git._remotes())
	#print(git.commitstamp('/home/d0n/cfg/home/USER/.vimrc'))
	#os.chdir('bin')
	#repo = GitSync()
	#print(repo.gitsync('master'))
