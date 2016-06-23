#!/usr/bin/env python3
from os.path import \
    expanduser as _expanduser, \
    basename as _basename

from tarfile import \
    open as taropen

from tempfile import \
    NamedTemporaryFile as _NamedTemporaryFile

from .gpg import GPGTool

gpg = GPGTool()

def envault(folder, *recipients, target=None):
	fingers = list(gpg.export(*recipients, **{'typ': 'e'}))
	target = target if target else '%s.vault'%_basename(folder)
	with _NamedTemporaryFile() as tmp:
		with taropen(tmp.name, "w:gz") as tar:
			tar.add(folder, arcname=_basename(folder))
		tmp.seek(0)
		gpg.encrypt(tmp.read(), fingers, output=target)

def unvault(vault, target=None):
	target = target if target else '%s'%_basename(vault).split('.')[0]
	with _NamedTemporaryFile() as tmp:
		with open(vault, 'rb') as vlt:
			gpg.decrypt(vlt.read(), tmp.name)
		tmp.seek(0)
		with taropen(tmp.name, "r:gz") as tar:
			tar.extractall(target)

if __name__ == '__main__':
	exit(1)
