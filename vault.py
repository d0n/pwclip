#!/usr/bin/env python3
from os.path import \
    isdir as _isdir, \
    basename as _basename, \
    expanduser as _expanduser

from tarfile import \
    open as taropen

from tempfile import \
    NamedTemporaryFile as _NamedTemporaryFile

from .gpg import GPGTool



class WeakVaulter(GPGTool):
	source = '~/.weaknez'
	crypt = '~/.vault'
	target = '~/'
	def envault(self, source, *recipients, target=None):
		"""
		envaulting function takes source to envault and additionally
		may search for any given pattern as recipients for encryption
		otherwise uses all found in keyring 
		"""
		fingers = list(self.export(*recipients, **{'typ': 'e'}))
		target = target if target else self.target
		with _NamedTemporaryFile() as tmp:
			with taropen(tmp.name, "w:gz") as tar:
				tar.add(source, arcname=_basename(source))
			tmp.seek(0)
			self.encrypt(tmp.read(), fingers, output=target)

	def unvault(self, vault, target=None):
		"""
		unvaulting function takes a vault as input and tries to decrypt it
		using all known recipients in the keyring optionally takes a target
		folder as output for decrypted data
		"""
		with _NamedTemporaryFile() as tmp:
			with open(vault, 'rb') as vlt:
				self.decrypt(vlt.read(), tmp.name)
			tmp.seek(0)
			with taropen(tmp.name, "r:gz") as tar:
				if target:
					tar.extractall(target)
				else:
					tar.extractall()

	def weakvault(self, mode=None):
		if not mode:
			if _isdir(self.weaks):
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

if __name__ == '__main__':
	exit(1)
