#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from os.path import \
    expanduser as _expanduser, \
    walk as _walk

from gnupg import GPG as _GPG
import tarfile


class GPGTool(object):
	_dbg = False
	gpg = _GPG()
	tar = tarfile
	vault = _expanduser('~/.vault')
	weakz = _expanduser('~/.weaknez')
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in GPGTool.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                GPGTool.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(GPGTool.__dict__.items())),
                GPGTool.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	def _entar(self, target):
		tar = self.tar.open(self.vault, "w:gz")
		for (dirs, subs, files) in _walk(target):
			for dat in files:
				tar.add('%s/%s'%(dirs, dat))
		tar.close()
		return self.vault

	def _untar(self, target):
		tar = self.tar.open(target, "r:gz"):
		tar.extractall()
		tar.close()

	def identities(self):
		"""return list of known identies (in keyring)"""
		return [i for i in [u['uids'] for u in self.gpg.list_keys()]]

	def encrypt(self):
		pass
	
	def decrypt(self):
		pass

