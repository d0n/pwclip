#!/usr/bin/env python3
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""gpg.py main program"""
import os
import io
import sys
from . import _gpgme
#from StringIO import StringIO

"""
    >>> Context
    >>> GenkeyResult
    >>> GpgmeError
    >>> ImportResult
    >>> Key
    >>> KeyIter
    >>> KeySig
    >>> NewSignature
    >>> Signature
    >>> Subkey
    >>> UserId
    >>> __doc__
    >>> __file__
    >>> __loader__
    >>> __name__
    >>> __package__
    >>> __spec__
    >>> gpgme_version
    >>> make_constants
"""
from .melibout import libout

class PrettyGoodPrivacy(type(_gpgme)):
	_dbg = False
	_gpgme.make_constants(globals())
	_armor = True
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		mod = [m for m in sys.modules if str(m).endswith('_gpgme')][0]
		for sub in dir(sys.modules[mod]):
			setattr(self, sub, getattr(_gpgme, sub))
		if self.dbg:
			lim = int(max(len(k) for k in PrettyGoodPrivacy.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                PrettyGoodPrivacy.__mro__,
                '\n'.join('  %s%s=\t%s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(PrettyGoodPrivacy.__dict__.items())),
                PrettyGoodPrivacy.__init__,
                '\n'.join('  %s%s=\t%s'%(k, ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if isinstance(val, bool) is bool else self._dbg

	@property                # armor <bool>
	def armor(self):
		return self._armor
	@armor.setter
	def armor(self, val):
		self._armor = val if isinstance(val, bool) is bool else self._armor

	@property                # gpg <object>
	def __gpg(self):
		ctx = self.Context()
		ctx.armor = self.armor
		return ctx

	@staticmethod
	def __getstream(path):
		with open(path, 'rb') as dat:
			return dat.read()

	@staticmethod
	def _normalize(data, armor=False):
		if armor:
			 norm = data.read().decode()
		else:
			norm = data.getvalue().decode()
		return norm

	def _fpr(self, pattern=None):
		for key in self.__gpg.keylist(pattern, False):
			return key.subkeys[0].fpr

	def decrypt(self, crypt, bits=False, stream=True):
		if stream:
			crypt = crypt.encode()
		if not bits:
			crypt = io.BytesIO(crypt)
		#armor.seek(0)
		plain = io.BytesIO()
		#print(crypt, plain)
		self.__gpg.decrypt(crypt, plain)
		return plain

	def encrypt(self, data, user, stream=True):
		data = data.encode() if stream else self.__getsteam(data)
		plain = io.BytesIO(data)
		crypt = io.BytesIO()
		user = self.__gpg.get_key(self._fpr(user))
		#print(user, 0, plain, self.armor)
		self.__gpg.encrypt([user], 0, plain, crypt)
		crypt.seek(0)
		return crypt

	def keyrings(self):
		keyrings = {}
		for keyring in self.__gpg.keylist():
			keys = {}
			for key in keyring.subkeys:
				features = []
				if key.can_authenticate:
					features.append('auth')
				if key.can_certify:
					features.append('cert')
				if key.can_encrypt:
					features.append('encrypt')
				if key.can_sign:
					features.append('sign')
				keys[key.fpr] = features
			keyrings[keyring.uids[0].name] = {
                'mail': keyring.uids[0].email, 'keys': keys}
		return keyrings










def main():
	gpg = PrettyGoodPrivacy()
	#print(gpg.keyrings())
	crypt = gpg.encrypt('bla', 'd0nback', stream=True)
	pabel = gpg._normalize(crypt)
	plain = gpg.decrypt(pabel)
	plout = gpg._normalize(plain)
	print(crypt)
	print(pabel)
	print(plain)
	print(plout)












