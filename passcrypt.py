#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""passcrypt module"""

from os import path, remove, environ, chmod, stat, utime

from shutil import copyfile

from yaml import load, dump

from paramiko.ssh_exception import SSHException

from time import time

from colortext import bgre, tabd

from system import userfind, fileage

from net.ssh import SecureSHell

from secrecy.gpg import GPGTool

class PassCrypt(GPGTool, SecureSHell):
	"""passcrypt main class"""
	dbg = None
	aal = None
	sho = None
	try:
		user = userfind()
		home = userfind(user, 'home')
	except FileNotFoundError:
		user = environ['USERNAME']
		home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])
	user = user if user else 'root'
	home = home if home else '/root'
	plain = path.join(home, '.pwd.yaml')
	crypt = path.join(home, '.passcrypt')
	remote = ''
	reuser = user
	recvs = []
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	if 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']] + [
            k for k in recvs if k != environ['GPGKEY']]
	__weaks = {}
	__oldweaks = {}
	def __init__(self, *args, **kwargs):
		"""passcrypt init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(PassCrypt.__mro__))
			print(bgre(tabd(PassCrypt.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		GPGTool.__init__(self, *args, **kwargs)
		SecureSHell.__init__(self, *args, **kwargs)
		write = False
		if self.remote and self._copynews_():
			write = True
		__weaks = self._readcrypt()
		self.__oldweaks = __weaks
		try:
			with open(self.plain, 'r') as pfh:
				__newweaks = load(pfh.read())
			if not self.dbg:
				remove(self.plain)
			write = True
		except FileNotFoundError:
			__newweaks = {}
		if __newweaks:
			__weaks = __weaks if __weaks else {}
			for (k, v) in __newweaks.items():
				__weaks[k] = v
		self.__weaks = __weaks
		if write:
			self._writecrypt(__weaks)

	def _copynews_(self):
		"""copy new file method"""
		if self.dbg:
			print(bgre(self._copynews_))
		now = int(time())
		try:
			age = fileage(self.crypt)
		except FileNotFoundError:
			age = 14401
		if age > 14400 and self.remote:
			try:
				return self.scpcompstats(
                    self.crypt, path.basename(self.crypt),
                    remote=self.remote, reuser=self.reuser, rotate=2)
			except FileNotFoundError:
				pass
			except SSHException as err:
				error(err)
			with open(tf, 'w+') as tfh:
				tfh.write(now)

	def _chkcrypt(self, __weak):
		"""crypt file checker method"""
		if self.dbg:
			print(bgre(self._chkcrypt))
		if self.__oldweaks == __weak:
			return True

	def _findentry(self, pattern, __weak):
		"""entry finder method"""
		if self.dbg:
			print(bgre(tabd({self._findentry: {'pattern': pattern}})))
		for (u, p) in __weak.items():
			if pattern == u or (
                  len(p) == 2 and len(pattern) > 1 and pattern in p[1]):
				return p

	def _readcrypt(self):
		"""read crypt file method"""
		if self.dbg:
			print(bgre(self._readcrypt))
		try:
			with open(self.crypt, 'r') as vlt:
				crypt = vlt.read()
		except FileNotFoundError:
			return None
		return load(str(self.decrypt(crypt)))

	def _writecrypt(self, __weak):
		"""crypt file writing method"""
		if self.dbg:
			print(bgre(self._writecrypt))
		kwargs = {'output': self.crypt}
		if self.recvs:
			kwargs['recipients'] = self.recvs
		for i in range(0, 4):
			self.encrypt(message=dump(__weak), **kwargs)
			if self._chkcrypt(__weak):
				chmod(self.crypt, 0o600)
				if self.remote:
					self._copynews_()
				break
		return True

	def adpw(self, usr, pwd=None):
		"""password adding method"""
		if self.dbg:
			print(bgre(tabd({
                self.adpw: {'user': self.user, 'entry': usr, 'pwd': pwd}})))
		pwdcom = [pwd if pwd else self._passwd()]
		com = input('enter a comment: ')
		if com:
			pwdcom.append(com)
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.adpw, usr, pwd))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys():
			__weak[self.user][usr] = pwdcom
			self._writecrypt(__weak)
			return True

	def chpw(self, usr, pwd=None):
		"""change existing password method"""
		if self.dbg:
			print(bgre(tabd({
                self.chpw: {'user': self.user, 'entry': usr, 'pwd': pwd}})))
		pwdcom = [pwd if pwd else self._passwd()]
		com = input('enter a comment: ')
		if com:
			pwdcom.append(com)
		if self.dbg:
			print('%s\n adduser = %s addpass, comment = %s'%(
                self.chpw, usr, pwdcom))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys() and \
              usr in __weak[self.user].keys():
			__weak[self.user][usr] = pwdcom
			self._writecrypt(__weak)
			return True

	def rmpw(self, usr):
		"""remove password method"""
		if self.dbg:
			print(bgre(tabd({self.rmpw: {'user': self.user, 'entry': usr}})))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys() and \
              usr in __weak[self.user].keys():
			del __weak[self.user][usr]
			if self._writecrypt(__weak):
				if self.remote:
					self._copynews_()
			return True

	def lspw(self, usr=None, aal=None):
		"""password listing method"""
		if self.dbg:
			print(bgre(tabd({self.lspw: {'user': self.user, 'entry': usr}})))
		aal = True if aal else self.aal
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					for (user, _) in self.__weaks.items():
						__match = self._findentry(usr, self.__weaks[user])
						if __match:
							__ents = {usr: __match}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr:
					__ents = {usr: self._findentry(usr, __ents)}
			return __ents

def lscrypt(usr, dbg=None):
	"""passlist wrapper function"""
	if dbg:
		print(bgre(lscrypt))
	if usr:
		return PassCrypt().lspw(usr)




if __name__ == '__main__':
	exit(1)
