#!/usr/bin/env python3

from os import path, remove, environ, chmod

try:
	from os import uname
except ImportError:
	def uname(): return [_, environ['COMPUTERNAME']]

from tarfile import open as taropen

from yaml import load, dump

from time import sleep

from shutil import copyfile

from paramiko.ssh_exception import SSHException

from colortext import bgre, tabd, error, fatal

from system import userfind

from net.util import SecureSHell as SSH

from secrecy.gpg import GPGTool

from secrecy.yubi import ykchalres

class PassCrypt(GPGTool):
	dbg = False
	aal = False
	sho = False
	try:
		user = userfind()
		home = userfind(user, 'home')
	except FileNotFoundError:
		user = environ['USERNAME']
		home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])
	plain = '%s/.pwd.yaml'%home
	crypt = '%s/.passcrypt'%home
	recvs = []
	remote = ''
	reuser = user
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = recvs + [
            environ['GPGKEY']] if not environ['GPGKEY'] in recvs else []
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(PassCrypt.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		self._copynews_()
		__weaks = self._readcrypt()
		if path.exists(self.crypt) and __weaks is None:
			self._garr()
			__weaks = self._readcrypt()
		try:
			with open(self.plain, 'r') as pfh:
				__newpws = load(pfh.read())
			remove(self.plain)
		except FileNotFoundError:
			__newpws = {}
		if __newpws:
			__weaks = __weaks if __weaks else {}
			for (k, v) in __newpws.items():
				__weaks[k] = v
		if __weaks != self._readcrypt():
			self._writecrypt_(__weaks)
		self.__weaks = __weaks


	def _copynews_(self):
		if self.remote:
			try:
				SSH().scpcompstats(
                    self.crypt, path.basename(self.crypt),
                    self.remote, self.reuser)
			except FileNotFoundError:
				pass

	def _chkcrypt(self):
		if self._readcrypt() == self.__weaks:
			return True

	def _findentry(self, pattern, weaks=None):
		__weaks = weaks if weaks else self.__weaks
		for (u, p) in __weaks.items():
			if pattern == u or (
                  len(p) == 2 and len(pattern) > 1 and pattern in p[1]):
				return p

	def _readcrypt(self):
		if self.dbg:
			print('%s\n  crypt = %s'%(self._readcrypt, self.crypt))
		try:
			with open(self.crypt, 'r') as vlt:
				crypt = vlt.read()
		except FileNotFoundError:
			return None
		return load(str(self.decrypt(crypt)))

	def _writecrypt_(self, plain):
		if self.dbg:
			print('%s\n  weaknez = %s'%(self._writecrypt, plain))
		kwargs = {'output': self.crypt}
		if self.recvs:
			kwargs['recipients'] = self.recvs
		self.__weaks = plain
		try:
			copyfile(self.crypt, '%s.1'%self.crypt)
			chmod('%s.1'%self.crypt, 0o600)
		except FileNotFoundError:
			pass
		while True:
			self.encrypt(message=dump(self.__weaks), **kwargs)
			if self._chkcrypt():
				self._copynews_()
				chmod(self.crypt, 0o600)
				break

	def adpw(self, usr, pwd=None):
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
			self._writecrypt_(__weak)
			return True

	def chpw(self, usr, pwd=None):
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
			self._writecrypt_(__weak)
			return True

	def rmpw(self, usr):
		if self.dbg:
			print('%s\n  user = %s\n  deluser = %s'%(
                self.rmpw, self.user, usr))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys() and \
              usr in __weak[self.user].keys():
			del __weak[self.user][usr]
			self._writecrypt_(__weak)
			return True

	def lspw(self, usr=None, aal=None, display=None):
		if self.dbg:
			print('%s\n  user = %s\n  getuser = %s'%(
                self.lspw, self.user, usr))
		aal = True if aal else self.aal
		sho = True if display else self.sho
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					for (user, entrys) in self.__weaks.items():
						__match = self._findentry(usr, self.__weaks[user])
						if __match:
							__ents = {usr: __match}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr:
					__ents = {usr: self._findentry(usr, __ents)}
			return __ents

def lscrypt(usr):
	if usr:
		return PassCrypt().lspw(usr)

if __name__ == '__main__':
    exit(1)
