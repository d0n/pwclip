#!/usr/bin/env python3
from os.path import \
    expanduser as _expanduser, \
    basename as _basename

from tarfile import \
    open as taropen

from tempfile import \
    NamedTemporaryFile as _NamedTemporaryFile

from .gpg import GPGTool


class WeakVaulter(GPGTool):
	def envault(self, folder, *recipients, target=None):
		fingers = list(self.export(*recipients, **{'typ': 'e'}))
		target = target if target else '%s.vault'%_basename(folder)
		with _NamedTemporaryFile() as tmp:
			with taropen(tmp.name, "w:gz") as tar:
				tar.add(folder, arcname=_basename(folder))
			tmp.seek(0)
			self.encrypt(tmp.read(), fingers, output=target)

	def unvault(self, vault, target=None):
		with _NamedTemporaryFile() as tmp:
			with open(vault, 'rb') as vlt:
				self.decrypt(vlt.read(), tmp.name)
			tmp.seek(0)
			with taropen(tmp.name, "r:gz") as tar:
				if target:
					tar.extractall(target)
				else:
					tar.extractall()

if __name__ == '__main__':
	exit(1)
