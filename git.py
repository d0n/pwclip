#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
import sys
# local relative imports
sys.path = [os.path.expanduser('~/bin')] + [
    p for p in sys.path if p != os.path.expanduser('~/bin')]
from modules.system.executor import Command
from modules.system.common import which, realpaths
from modules.colortext import blu, yel
# default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.path.abspath(os.readlink(os.path.dirname((__file__))))
__version__ = '0.1'

class GitRepo(Command):
	# Command class attribute
	_sh_ = True
	# own attributes
	_dbg = False
	_repodir = ''
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
		#super().__init__(*args, **kwargs)
	# rw propereties
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	@property               # repodir <str>
	def repodir(self):
		return self._repodir
	@repodir.setter
	def repodir(self, val):
		self._repodir = val if type(val) is str else os.getcwd()
	# ro properties
	@property               # gitbin <str>
	def gitbin(self):
		return self._gitbin

	def _gitdir(self):
		repodir = self._repodir if self._repodir else os.getcwd()
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
			command = self.gitbin, 'fetch', '--all'
		if self.erno(command) == 0:
			return True

	def _fetchref_(self):
		fetchead = '%s/FETCH_HEAD' %(self._gitdir())
		if os.path.isfile(fetchead):
			with open(fetchead, 'r') as f:
				return f.read().split('\t')[0].strip()

	def _headref_(self):
		hrefile = '%s/refs/heads/%s'%(self._gitdir(), self._head())
		if os.path.isfile(hrefile):
			with open(hrefile, 'r') as f:
				return f.read().split(' ')[0].strip()

	def _heads(self):
		if not os.path.exists('%s/refs/heads'%(self._gitdir())):
			errmsg = 'no basedir was set and current one is no git repo %s'%(
			    self._gitdir())
			raise RuntimeError(errmsg)
		return os.listdir('%s/refs/heads'%(self._gitdir()))

	def _head(self):
		with open('%s/HEAD'%(self._gitdir()), 'r') as f:
			return f.read().split('/')[-1].strip()

	def _remoteref(self):
		self._fetch_(fetchall=True)
		gitdir = self._gitdir()
		remref = '%s/refs/remotes/origin/%s'%(gitdir, self._head())
		if not os.path.isfile(remref):
			remref = '%s/refs/remotes/origin/HEAD'%(gitdir)
		with open(remref, 'r') as f:
			return f.read().strip()

	def _remotes(self):
		return [rem for rem in os.listdir(
		    '%s/refs/remotes/origin/'%(self._gitdir())) if rem != 'HEAD']

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
	_sh_ = True
	_ato = True
	@property               # ato <bool>
	def ato(self):
		return self._ato
	@ato.setter
	def ato(self, val):
		self._ato = val if type(val) is bool else self._ato

	def gitsync(self, *branchs, checkout=None, syncall=None):
		branchs = list(branchs)
		if not branchs:
			branchs = [self._head()]
		if syncall:
			branchs = branchs + [h for h in self._heads(
			    ) if not h in (self._head(), checkout)]
		if checkout:
			branchs = branchs + [checkout]
		for branch in branchs:
			if branch != self._head():
				self.checkout(branch)
			if self._isbehind():
				self.pull()
			status = self.gitstatus()
			if status:
				if self.ato:
					self.add()
					self.commit(status)
			commits = self.genmessage(status)
			if self._isahead():
				self.push()
		if checkout and not checkout == self._head():
			self.checkout(checkout)
		return commits




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
