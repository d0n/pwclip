#!/usr/bin/env python3

from os import path, uname

from tarfile import open as taropen

from yaml import load, dump

from tempfile import NamedTemporaryFile

from colortext import error, fatal

from system import userfind

from .gpg import GPGTool

class WeakVaulter(GPGTool):
	_dbg = False
	host = uname()[1]
	user = userfind()
	targets = path.expanduser('~/.weaknez')
	vltfile = path.expanduser('~/.vltfile')
	vault = path.expanduser('~/.pwds')
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '_%s'%arg):
				setattr(self, '_%s'%arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '_%s'%key):
				setattr(self, '_%s'%key, val)
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

	def _dumpvault(self, vault):
		if self.dbg:
			print('%s\n  vault = %s'%(self._dumpvault, vault))
		try:
			with open(vault, 'r') as vlt:
				return load(str(self.decrypt(vlt.read())))
		except FileNotFoundError:
			self._mkvault(vault)
			return self._readvault(vault)
		

	def _readvault(self, vault):
		if self.dbg:
			print('%s\n  vault = %s'%(self._readvault, vault))
		try:
			with open(vault, 'r') as vlt:
				return load(str(self.decrypt(vlt.read())))
		except FileNotFoundError:
			self._mkvault(vault)
			return self._readvault(vault)

	def _writevault(self, weaknez, vault):
		if self.dbg:
			print('%s\n  weaknez = %s'%(self._mkvault, weaknez))
		try:
			with open(vault, 'w+') as vlt:
				vlt.write(str(self.encrypt(dump(weaknez))))
		else:
			return True

	def _mkvault(self, vault):
		__newvault = '{%s: {%s: {}}}'%(self.host, self.user)
		if self.dbg:
			print('%s\n  vault = %s\n  weaknez = %s'%(
                self._mkvault, vault, __newvault))
		return self._writevault(__newvault, output=vault)

	def addpass(self, adduser, addpass, vault=None):
		vault = vault if vault else self.vault
		if self.dbg:
			print('%s\n  user = %s\n  host = %s\n  adduser = %s addpass = %s'%(
                self.addpass, self.host, self.user, adduser, addpass))
		__weak = self._readvault(vault)
		__weak[self.host][self.user][adduser] = addpass
		self._writevault(__weak, vault)

	def getpass(self, getuser, vault=None):
		vault = vault if vault else self.vault
		if self.dbg:
			print('%s\n  user = %s\n  host = %s\n  getuser = %s'%(
                self.getpass, self.host, self.user, getuser))
		__weak = self._readvault(vault)
		if getuser in __weak[self.host][self.user].keys():
			return __weak[self.host][self.user][getuser]



if __name__ == '__main__':
	exit(1)
