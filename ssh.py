#!/usr/bin/env python3
"""ssh connection and remote command """

#global imports"""
import os
import sys
import paramiko

# local relative imports
from socket import getfqdn as fqdn

# default vars
__version__ = '0.1'

class SecureSHell(object):
	_dbg = False
	_user = 'root'
	_host = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
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
		self._dbg = val if type(val) is bool else self._dbg
	@property               # host <str>
	def host(self):
		return self._host
	@host.setter
	def host(self, val):
		self._host = val if type(val) is str else self._host
	@property               # user <str>
	def user(self):
		return self._user
	@user.setter
	def user(self, val):
		self._user = val if type(val) is str else self._user

	def __auth(self, host=None):
		if not host:
			if not self.host:
				raise RuntimeError('cannot create transport without target host')
			host = self.host
		transport = paramiko.Transport((host, 22))
		transport.start_client()
		if transport and transport.is_authenticated():
			return True
		agent = paramiko.agent.Agent()
		keys = agent.get_keys()
		for key in keys:
			print(transport.auth_publickey(self.user, key))
		return transport

	def rstdo(self, cmd, host=None):
		if self.dbg:
			print('\033[01;30m%s\033[0m'%self.command)
		if not host:
			host = self.host
		host = fqdn(host)
		if not self.__auth(host):
			raise RuntimeError('could not authenticate')
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host, username=self.user)
		stdin, stdout, stderr = client.exec_command(cmd)
		return stdout.readlines() #, stderr.readlines()

	def scp(self, source, target, host=None, user=None):
		if not host:
			host = self.host
		if host:
			host = fqdn(host)
		if not user:
			user = self.user
		ssh = paramiko.SSHClient()
		#ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, 22, user)
		scp = ssh.open_sftp()
		return scp.put(source, target)





if __name__ == '__main__':
	"""module debugging area"""
	#ssh = SecureSHell(**{'host':'bigbox.janeiskla.de'})
	#print(ssh.command('cat /etc/debian_version'))
