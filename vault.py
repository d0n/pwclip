#!/usr/bin/env python3

from os import path, uname

from tarfile import open as taropen

from tempfile import NamedTemporaryFile

from colortext import error, fatal

from system import userfind

from .gpg import GPGTool

class WeakVaulter(GPGTool):
	_dbg = False
	target = path.expanduser('~/.weaknez')
	vault = path.expanduser('~/.vault')
	host = uname()[1]
	user = userfind()
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

	def envault(self, source, *recipients, target=None):
		"""
		envaulting function takes source to envault and additionally
		may search for any given pattern as recipients for encryption
		otherwise uses all found in keyring 
		"""
		fingers = list(self.export(recipients, typ='e'))
		target = target if target else self.target
		with NamedTemporaryFile() as tmp:
			with taropen(tmp.name, "w:gz") as tar:
				tar.add(source, arcname=path.basename(source))
			tmp.seek(0)
			self.encrypt(tmp.read(), fingers, output=target)

	def unvault(self, vault, target=None):
		"""
		unvaulting function takes a vault as input and tries to decrypt it
		using all known recipients in the keyring optionally takes a target
		folder as output for decrypted data
		"""
		with NamedTemporaryFile() as tmp:
			with open(vault, 'rb') as vlt:
				self.decrypt(vlt.read(), tmp.name)
			tmp.seek(0)
			with taropen(tmp.name, "r:gz") as tar:
				if target:
					tar.extractall(target)
				else:
					tar.extractall()

	def weakvault(self, mode=None):
		"""
		the weakvaulter method abstracts the other implied de/envualt methods
		"""
		if not mode:
			if path.isdir(self.weaks):
				mode = envault
				weakvault = self.source
			else:
				mode = unvault
				weakvault = self.crypt
		elif mode == 'envault':
			mode = envault
			weakvault = self.source
		elif mode == 'unvault':
			mode = unvault
			weakvault = self.crypt
		mode(weakvault)

	def vaulter(self, vault=None):
		vault = vault if vault else self.vault



if __name__ == '__main__':
	exit(1)
