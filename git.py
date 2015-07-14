#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
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
		command = self.gitbin, 'fetch'
		if fetchall:
			command = '%s fetch --all'%self.gitbin
		if self.erno(command) == 0:
			return True

	def _fetchref_(self):
		fetchead = '%s/FETCH_HEAD' %(self.gitdir)
		if os.path.isfile(fetchead):
			with open(fetchead, 'r') as f:
				return f.read().split('\t')[0].strip()

	def _headref_(self):
		hrefile = '%s/refs/heads/%s'%(self.gitdir, self._head())
		if os.path.isfile(hrefile):
			with open(hrefile, 'r') as f:
				return f.read().split(' ')[0].strip()

	def _heads(self):
		if not os.path.exists('%s/refs/heads'%(self.gitdir)):
			errmsg = 'no basedir was set and current one is no git repo %s'%(
                self.gitdir)
			raise RuntimeError(errmsg)
		return os.listdir('%s/refs/heads'%(self.gitdir))

	def _head(self):
		with open('%s/HEAD'%(self.gitdir), 'r') as f:
			return f.read().split('/')[-1].strip()

	def _remoteref(self):
		self._fetch_(fetchall=True)
		gitdir = self.gitdir
		remref = '%s/refs/remotes/origin/%s'%(gitdir, self._head())
		if not os.path.isfile(remref):
			remref = '%s/refs/remotes/origin/HEAD'%(gitdir)
		with open(remref, 'r') as f:
			return f.read().strip()

	def _remotes(self):
		return [rem for rem in os.listdir(
	        '%s/refs/remotes/origin/'%(self.gitdir)) if rem != 'HEAD']

	def _isbehind(self):
		if self._remoteref() != self._headref_():
			return True

	def _isahead(self):
		if self._headref_() != self._fetchref_():
			return True

	def checkout(self, branch, *files):
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
		command = '%s pull %s' %(self.gitbin, origin)
		return int(self.call(command))

	def push(self, remote=None, origin='origin', setup=None):
		if not remote:
			remote = self._head()
		command = '%s push %s %s'%(self.gitbin, origin, remote)
		if setup or remote not in self._remotes():
			command = '%s push --set-upstream %s %s'%(
                self.gitbin, origin, remote)
		return int(self.call(command))

	def add(self, *files):
		command = '%s add -A'%(self.gitbin)
		if files:
			command = '%s add %s'%(self.gitbin, ' '.join(f for f in files))
		return int(self.call(command))

	def commit(self, message):
		command = '%s commit -a -m "%s"' %(self.gitbin, message)
		return int(self.call(command))

	def commitstamp(self, rpofile):
		rpofile = realpaths(rpofile)
		stamp = self.stdo('%s log -1 --format=%%at %s'%(self.gitbin, rpofile))
		if stamp:
			stamp = stamp.strip()
			return int(stamp)

	def show(self, *args, **kwargs):
		cmd = '%s show' %(self.gitbin)
		if 'commitstamp' in args:
			cmd = '%s show -s --format=%%at' %(self.gitbin)
		return self.stdo(cmd).strip()

	def gitstatus(self, mode='--porcelain'):
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

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if isinstance(val, bool) is bool else self._dbg

	@property                # aal <bool>
	def aal(self):
		return self._aal
	@aal.setter
	def aal(self, val):
		self._aal = val if isinstance(val, bool) is bool else self._aal

	@staticmethod
	def gitsubs(repo):
		def _modpaths(gitdir):
			def __gitmods(modfile):
				with open(modfile, 'r') as gmf:
					modlines = gmf.readlines()
				return [
                    l.split('=')[1].strip() for l in modlines if 'path =' in l
                    ]
			modfile = '%s/.gitmodules'%gitdir
			if os.path.isfile(modfile):
				return ['%s/%s'%(gitdir, m) for m in __gitmods(modfile)]
		mods = _modpaths(repo)
		if mods:
			return self.gitsubs(mods) + repo
		return repo

	def gitsync(
          self, branchs=['master'], mode='sync', checkout=None, syncall=None):
		if self.dbg:
			print(self.gitsync)
		syncall = syncall if syncall else self.aal
		_head = self._head()
		branchs = list(branchs) if branchs else [_head]
		if syncall:
			branchs = [h for h in self._heads() if h != checkout]
		branchs = [b for b in branchs if b != checkout] + [
            checkout if checkout else _head]
		branchstats = {}
		for branch in branchs:
			self.checkout(branch)
			if mode in ('sync', 'push'):
				status = self.gitstatus()
				if status:
					self.add()
					self.commit(status)
					branchstats[branch] = status
			if mode in ('sync', 'pull'):
				if self._isbehind():
					self.pull()
			if mode in ('sync', 'push'):
				if self._isahead():
					self.push()
		if branchstats != {}:
			return branchstats

"""
	def itergits(self, *branchs, remode='sync', syncall=None):
		if self.dbg:
			print(self.itergits)
		branchs = branchs if branchs else ['master']
		for sub in self.gitsubs(os.getcwd()):
			self.gitsync(mode=remode)

			if self.aal:
				yield self.gitsync(self._heads(), mode=remode)
			yield self.gitsync(mode=remode)
"""

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
