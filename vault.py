#!/usr/bin/env python3

from os import path, uname

from tarfile import open as taropen

from yaml import load, dump

from tempfile import NamedTemporaryFile

from colortext import error, fatal

from system import userfind

from .gpg import GPGTool

class WeakVaulter(GPGTool):
	dbg = False
	host = uname()[1]
	user = userfind()
	weaks = path.expanduser('~/.weaknez')
	vault = path.expanduser('~/.vault')
	crypt = '%s/common/pwd.vlt'%weaks
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
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

	def envault(self, source, *recipients, targets=None):
		"""
		envltfileing function takes source to envltfile and additionally
		may search for any given pattern as recipients for encryption
		otherwise uses all found in keyring 
		"""
		fingers = list(self.export(recipients, typ='e'))
		targets = targets if targets else self.targets
		with NamedTemporaryFile() as tmp:
			with taropen(tmp.name, "w:gz") as tar:
				tar.add(source, arcname=path.basename(source))
			tmp.seek(0)
			self.encrypt(tmp.read(), fingers, output=targets)

	def unvault(self, vltfile, targets=None):
		"""
		unvltfileing function takes a vltfile as input and tries to decrypt it
		using all known recipients in the keyring optionally takes a targets
		folder as output for decrypted data
		"""
		with NamedTemporaryFile() as tmp:
			with open(vltfile, 'rb') as vlt:
				self.decrypt(vlt.read(), tmp.name)
			tmp.seek(0)
			with taropen(tmp.name, "r:gz") as tar:
				if targets:
					tar.extractall(targets)
				else:
					tar.extractall()

	def weakvault(self, mode=None):
		"""
		the weakvltfileer method abstracts the other implied de/envualt methods
		"""
		if not mode:
			if path.isdir(self.weaks):
				mode = envltfile
				weakvltfile = self.source
			else:
				mode = unvltfile
				weakvltfile = self.crypt
		elif mode == 'envltfile':
			mode = envltfile
			weakvltfile = self.source
		elif mode == 'unvltfile':
			mode = unvltfile
			weakvltfile = self.crypt
		mode(weakvltfile)

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
		if self.dbg:
			print('%s\n  crypt = %s\n  weaknez = %s'%(
                self._mkcrypt, crypt, __newcrypt))
		return self._writecrypt(__newcrypt, crypt)

	def addpass(self, adduser, addpass, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.addpass, adduser, addpass))
		try:
			__weak = load(self._readcrypt(crypt))
		except (TypeError, AttributeError):
			__weak = self._readcrypt(crypt)
		print(__weak)
		__weak[self.user][adduser] = addpass
		return self._writecrypt(__weak, crypt)

	def delpass(self, deluser, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  user = %s\n  deluser = %s'%(
                self.delpass, self.user, deluser))
		try:
			__weak = load(self._readcrypt(crypt))
		except (TypeError, AttributeError):
			__weak = self._readcrypt(crypt)
		print(__weak)
		del __weak[self.user][deluser]
		return self._writecrypt(__weak)

	def getpass(self, getuser, crypt=None):
		crypt = crypt if crypt else self.crypt
		if self.dbg:
			print('%s\n  user = %s\n  host = %s\n  getuser = %s'%(
                self.getpass, self.user, getuser))
		__weak = self._readcrypt(crypt)
		print(__weak)
		__weak = __weak[self.user]
		return __weak[getuser]



if __name__ == '__main__':
	exit(1)
