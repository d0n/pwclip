#!/usr/bin/env python3
"""ssh connection and remote command """

#global imports"""
import os
import sys
from paramiko import ssh_exception, SSHClient, AutoAddPolicy
from shutil import copy2
from socket import getfqdn as fqdn, gaierror as NameResolveError

from colortext import bgre, tabd, abort, error, fatal
from system.user import whoami

# default vars
__version__ = '0.1'

class SecureSHell(object):
	_dbg = False
	reuser = ''
	remote = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '_%s'%(arg)):
				setattr(self, '_%s'%(arg), True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(SecureSHell.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if val else False

	@staticmethod
	def _ssh_(remote, user=None, port=22):
		_user = whoami()
		if '@' in remote:
			_user, remote = remote.split('@')
		user = _user if not user else user
		ssh = SSHClient()
		ssh.set_missing_host_key_policy(AutoAddPolicy())
		try:
			ssh.connect(fqdn(remote), int(port), username=user)
		except ssh_exception.SSHException as err:
			#print(bgre('h: %s, u: %s p: %s'%(remote, user, port)))
			fatal(err)
		except NameResolveError as err:
			#print(bgre('h: %s, u: %s p: %s'%(remote, user, port)))
			fatal(err)
		return ssh

	def rstdo(self, cmd, remote=None, user=None):
		remote = remote if remote else self.remote
		#print(remote)
		user = user if user else self.reuser
		if self.dbg:
			print(bgre(self.rstdo))
			print(bgre('  %s %s %s'%(user, remote, cmd)))
		ssh = self._ssh_(remote, user)
		_, out, _ = ssh.exec_command(cmd)
		return ''.join(out.readlines())

	def get(self, src, trg, remote=None, user=None):
		if self.dbg:
			print(bgre(self.get))
		user = user if user else self.reuser
		remote = remote if remote else self.remote
		if not (os.path.isfile(src) or os.path.isfile(trg)):
			raise FileNotFoundError('connot find either %s nor %s'%(src, trg))
		ssh = self._ssh_(remote, user)
		scp = ssh.open_sftp()
		return scp.get(src, trg)

	def put(self, src, trg, remote=None, user=None):
		if self.dbg:
			print(bgre(self.put))
		user = user if user else self.reuser
		remote = remote if remote else self.remote
		if not (os.path.isfile(src) or os.path.isfile(trg)):
			raise FileNotFoundError('connot find either %s nor %s'%(src, trg))
		ssh = self._ssh_(remote, user)
		scp = ssh.open_sftp()
		return scp.put(src, trg)

	def rcompstats(self, src, trg, remote=None, user=None):
		if self.dbg:
			print(bgre(self.rcompstats))
		remote = remote if remote else self.remote
		user = user if user else self.reuser
		smt = int(str(int(os.stat(src).st_mtime))[:6])
		rmt = self.rstdo(
            'stat -c %%Y %s'%trg, remote=remote, user=user)
		if rmt:
			rmt = int(str(rmt)[:6])
		if rmt == smt:
			return
		srctrg = src, '%s@%s:%s'%(user, remote, trg)
		if rmt and int(rmt) > int(smt):
			srctrg = '%s@%s:%s'%(user, remote, trg), src
		return srctrg

	def _localstamp(self, trg):
		if self.dbg:
			print(bgre(self._localstamp))
		return int(os.stat(trg).st_atime), int(os.stat(trg).st_mtime)
	
	def _remotestamp(self, trg, remote, user):
		if self.dbg:
			print(bgre(self._remotestamp))
		tat = self.rstdo(
            'stat -c %%X %s'%trg, remote, user)
		tmt = self.rstdo(
            'stat -c %%Y %s'%trg, remote, user)
		if tat and tmt: return int(tat), int(tmt)
		return None, None

	def _setlstamp(self, trg, atime, mtime):
		if self.dbg:
			print(bgre(self._setlstamp))
		os.utime(trg, (atime, mtime))

	def _setrstamp(self, trg, atime, mtime, remote, user):
		if self.dbg:
			print(bgre(self._setrstamp))
		self.rstdo(
            'touch -a --date=@%s %s'%(atime, trg), remote, user)
		self.rstdo(
            'touch -m --date=@%s %s'%(mtime, trg), remote, user)

	def scpcompstats(self, lfile, rfile, remote=None, user=None):
		if self.dbg:
			print(bgre(self.scpcompstats))
		user = user if user else self.reuser
		remote = remote if remote else self.remote
		lat, lmt = self._localstamp(lfile)
		rat, rmt = self._remotestamp(rfile, remote, user)
		if rmt == lmt:
			return
		elif rmt and rmt > lmt:
			copy2(lfile, '%s.1'%lfile)
			self.get(rfile, lfile, remote, user)
			self._setlstamp(lfile, rat, rmt)
		else:
			self.put(lfile, rfile, remote, user)
			self._setrstamp(rfile, lat, lmt, remote, user)




if __name__ == '__main__':
	"""module debugging area"""
	#ssh = SecureSHell(**{'remote':'bigbox.janeiskla.de'})
	#print(ssh.command('cat /etc/debian_version'))
