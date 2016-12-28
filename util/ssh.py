#!/usr/bin/env python3
"""ssh connection and remote command """

#global imports"""
import os
import sys
import paramiko

# local relative imports
from socket import getfqdn as fqdn

from colortext import abort

# default vars
__version__ = '0.1'

class SecureSHell(object):
	_dbg = False
	user = 'root'
	host = ''
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
			print('\033[01;30m%s\033[0m'%SecureSHell.__mro__)
			for (key, val) in self.__dict__.items():
				print('\033[01;30m%s = %s\033[0m'%(key, val))
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if val else False

	@staticmethod
	def _ssh_(host, user, port=22):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(host, int(port), username=user)
		except paramiko.ssh_exception.SSHException as err:
			print(err)
		return ssh

	def rstdo(self, cmd, host=None, user=None):
		host = host if host else self.host
		user = user if user else self.user
		ssh = self._ssh_(host, user)
		try:
			_, out, _ = ssh.exec_command(cmd)
		except KeyboardInterrupt:
			abort()
		return ''.join(out.readlines())

	def scp(self, src, trg, host=None, user=None):
		user = user if user else self.user
		host = host if host else self.host
		host = fqdn(host)
		ssh = self._ssh_(host, user)
		scp = ssh.open_sftp()
		return scp.put(src, trg)

	def compstats(self, src, trg, host=None, user=None):
		host = host if host else self.host
		user = user if user else self.user
		smt = int(str(int(os.stat(src).st_mtime))[:6])
		rmt = self.rstdo(
            'stat -c %%Y %s'%os.path.basename(src), host=host, user=user)
		if rmt:
			rmt = int(str(rmt)[:6])
		if rmt == smt:
			return
		srctrg = src, '%s@%s:%s'%(user, host, trg)
		if int(rmt) > int(smt):
			srctrg = '%s@%s:%s'%(user, host, trg), src
		return srctrg

	def scpcompstats(self, src, trg, host=None, user=None):
		user = user if user else self.user
		host = host if host else self.host
		smt = int(str(int(os.stat(src).st_mtime))[:6])
		rmt = self.rstdo(
            'stat -c %%Y %s'%os.path.basename(src), host=host, user=user)
		if rmt:
			rmt = int(str(rmt)[:6])
		if rmt == smt:
			return
		elif int(rmt) > int(smt):
			return self.scp(trg, src, host=host, user=user)
		return self.scp(src, trg, host=host, user=user)




if __name__ == '__main__':
	"""module debugging area"""
	#ssh = SecureSHell(**{'host':'bigbox.janeiskla.de'})
	#print(ssh.command('cat /etc/debian_version'))
