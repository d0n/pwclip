#!/usr/bin/env python3

from os import \
    path, uname, environ, \
    remove, symlink, chdir, \
    getcwd, readlink

from shutil import copyfile, rmtree, move

from tarfile import open as taropen

from yaml import load, dump

from tempfile import NamedTemporaryFile

from colortext import error, fatal

from network import SecureSHell as SSH

from netz import ping

from system import userfind

from secrecy.gpg import GPGTool

from executor import command as cmd

class WeakVaulter(GPGTool):
	dbg = False
	ruser = 'd0n'
	remot = 'janeiskla.de'
	weaks = '~/.weaknez'
	vault = '~/.vault'
	recvs = []
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		setattr(self, 'vault', path.expanduser(self.vault))
		setattr(self, 'weaks', path.expanduser(self.weaks))
		self._fixlns()
		if self.dbg:
			lim = int(max(len(k) for k in WeakVaulter.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                WeakVaulter.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(WeakVaulter.__dict__.items())),
                WeakVaulter.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))

	@staticmethod
	def _stopagent_():
		cmd.erno('killall -u %s -9 gpg-agent dirmngr scdaemon'%userfind())
		cmd.erno('rm %s/.gnupg/S.*'%path.expanduser('~/'))

	@staticmethod
	def _startagent_():
		if getuid() == 0:
			cmd.erno('su -l %s -c "gpg-agent --daemon"'%userfind())
		cmd.erno('gpg-agent --daemon')

	def _chkvlt(self):
		gpghead = '-----BEGIN PGP MESSAGE-----'
		gpgtail = '-----END PGP MESSAGE-----'
		with open(self.vault, 'r') as vlt:
			vlts = vlt.readlines()
		return ( vlts[0].strip() == gpghead and vlts[-1].strip() == gpgtail )

	def _fixlns(self):
		self._stopagent_()
		_home = path.expanduser('~/').rstrip('/')
		for ln in ('.gnupg', '.ssh', '.vpn'):
			if ( path.islink('%s/%s'%(_home, ln)) and not \
                  path.isdir(readlink('%s/%s'%(_home, ln)))):
				remove(ln)
				try:
					move('%s/%s.1'%(_home, ln), '%s/%s'%(_home, ln))
				except FileNotFoundError:
					pass
		self._startagent_()

	def _mklns(self):
		self._stopagent_()
		_home = path.expanduser('~/').rstrip('/')
		_host = uname()[1]
		pwd = getcwd()
		chdir(_home)
		for ln in ('.gnupg', '.ssh', '.vpn'):
			trg = '%s/%s/%s'%(path.basename(self.weaks), _host, ln)
			if path.isdir(path.expanduser('~/%s'%trg)):
				try:
					move('%s/%s'%(_home, ln), '%s/%s.1'%(_home, ln))
				except FileNotFoundError:
					pass
			if path.isdir('%s/%s'%(_home, trg)):
				symlink(trg, ln)
		chdir(pwd)
		self._startagent_()

	def _sync(self):
		if ping(self.remot):
			_stat = cmd.stdo('ssh %s@%s stat -c %%s %s'%(
                self.ruser, self.remot, self.vault))
			rstat = 0 if not _stat else int(_stat.strip())
			lstat = int(cmd.stdo('stat -c %%s %s'%(self.vault)).strip())
			if lstat < rstat:
				cmd.call('scp -B %s@%s:%s %s'%(
                    self.ruser, self.remot, self.vault, self.vault))
		elif self.remot:
			error('could not reach', self.remot)

	def envault(self):
		"""weaks (directory) envaulting (encryption) to vault (file) method"""
		fingers = list(self.export(*self.recvs, typ='e'))
		copyfile(self.vault, '%s.1'%self.vault)
		self._sync()
		with NamedTemporaryFile() as tmp:
			with taropen(tmp.name, "w:gz") as tar:
				tar.add(self.weaks, arcname=path.basename(self.weaks))
			tmp.seek(0)
			self.encrypt(
                tmp.read(), fingers, output=self.vault)
		if self._chkvlt():
			rmtree(self.weaks)
			self._fixlns()

	def unvault(self):
		"""unvaulting (decrypt vault file) to weaks (directory) method"""
		_home = path.expanduser('~/').rstrip('/')
		pwd = getcwd()
		chdir(_home)
		with NamedTemporaryFile() as tmp:
			with open(self.vault, 'rb') as vlt:
				self.decrypt(vlt.read(), tmp.name)
			tmp.seek(0)
			with taropen(tmp.name, "r:gz") as tar:
				tar.extractall()
		self._mklns()
		chdir(pwd)

	def weakvault(self):
		"""
		unvault (decrypt) if weaks (directory) does not exist otherwise
		envault (to vault file)
		"""
		if path.isdir(self.weaks):
			self.envault()
		else:
			self.unvault()





if __name__ == '__main__':
	exit(1)
