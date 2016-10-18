#!/usr/bin/env python3

from os import path, uname

from tarfile import open as taropen

from yaml import load, dump

from tempfile import NamedTemporaryFile

from colortext import error, fatal

from system import userfind

from .gpg import GPGTool

class PassCrypt(GPGTool):
	dbg = False
	user = userfind()
	home = userfind(user, 'home')
	plain = '%s/.pwd.yml'%home
	crypt = '%s/.pwd.vlt'%home
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in PassCrypt.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                PassCrypt.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(PassCrypt.__dict__.items())),
                PassCrypt.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))

	def _dumpcrypt(self, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  crypt = %s'%(self._dumpcrypt, crypt))
		try:
			with open(crypt, 'r') as vlt:
				return load(str(self.decrypt(vlt.read())))
		except FileNotFoundError:
			self._mkcrypt(crypt)
			return self._readcrypt(crypt)

	def _readcrypt(self, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  crypt = %s'%(self._readcrypt, crypt))
		try:
			with open(crypt, 'r') as vlt:
				return load(str(self.decrypt(vlt.read())))
		except FileNotFoundError:
			self._mkcrypt(crypt)
			return self._readcrypt(crypt)

	def _writecrypt(self, weaknez, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  weaknez = %s'%(self._writecrypt, weaknez))
		with open(crypt, 'w+') as vlt:
			vlt.write(str(self.encrypt(dump(weaknez))))
		return True

	def _mkcrypt(self, crypt=None):
		crypt = crypt if crypt else self.crypt
		__newcrypt = '{%s: {}}'%self.user
		if path.exists(self.plain):
			with open(self.plain, 'r') as pfh:
				__newcrypt = load(pfh)
		if self.dbg:
			print('%s\n  crypt = %s\n  weaknez = %s'%(
                self._mkcrypt, crypt, __newcrypt))
		return self._writecrypt(__newcrypt, crypt)

	def adpw(self, usr, pwd, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.adpw, user, pwd))
		try:
			__weak = load(self._readcrypt(crypt))
		except (TypeError, AttributeError):
			__weak = self._readcrypt(crypt)
		__weak[self.user][usr] = pwd
		return self._writecrypt(__weak, crypt)

	def chpw(self, usr, pwd, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.chpw, usr, pwd))
		try:
			__weak = load(self._readcrypt(crypt))
		except (TypeError, AttributeError):
			__weak = self._readcrypt(crypt)
		__weak[self.user][usr] = pwd
		return self._writecrypt(__weak, crypt)

	def rmpw(self, usr, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  user = %s\n  deluser = %s'%(
                self.rmpw, self.user, usr))
		try:
			__weak = load(self._readcrypt(crypt))
		except (TypeError, AttributeError):
			__weak = self._readcrypt(crypt)
		del __weak[self.user][usr]
		return self._writecrypt(__weak)

	def lspw(self, usr=None, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  user = %s\n  getuser = %s'%(
                self.lspw, self.user, usr))
		__weaks = self._readcrypt(crypt)[self.user]
		if not usr:
			return __weaks
		for (u, p) in __weaks.items():
			if usr == u:
				return p


if __name__ == '__main__':
    exit(1)
