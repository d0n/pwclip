#!/usr/bin/env python3
"""
gpgtool module
"""
# -*- encoding: utf-8 -*-

# (std)lib imports
from os import \
    X_OK as _XOK, \
    access as _access, \
    getcwd as _getcwd

from os.path import \
    isfile as _isfile, \
    expanduser as _expanduser

from getpass import \
    getpass as _getpass

from gnupg import \
    GPG as _GPG

# local imports
from colortext import blu, red, yel, bgre, abort, error

class GPGTool(object):
	"""
	gnupg wrapper-wrapper :P
	although the gnupg module is quite handy and the functions are pretty and
	useable i need some modificated easing functions to be able to make the
	main code more easy to understand by wrapping multiple gnupg functions to
	one - also i can prepare some program related stuff in here
	"""
	_dbg = False
	_homedir = _expanduser('~/.gnupg')
	_binary = '/usr/bin/gpg2'
	_keyring = '%s/pubring.kbx'%_homedir
	if not _isfile(_binary):
		_binary = '/usr/bin/gpg'
	kginput = {}
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
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
                '\n'.join('  %s%s=    %s'%(k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		"""bool"""
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	@property                # homedir <str>
	def homedir(self):
		return self._homedir
	@homedir.setter
	def homedir(self, val):
		self._homedir = val if not val.startswith('~') else _expanduser(val)
		if not self._homedir.startswith('/'):
			self._homedir = '%s/%s'%(_getcwd(), val)

	@property                # gpgbin <str>
	def binary(self):
		"""string"""
		return self._binary
	@binary.setter
	def binary(self, val):
		if _isfile(val) and _access(val, _XOK):
			self._binary = val
		if not _isfile(self._binary) or not _access(self._binary, _XOK):
			raise RuntimeError('%s needs to be executable'%self._binary)

	@property                # _gpg_ <GPG>
	def _gpg_(self):
		"""object"""
		#return _GPG(gnupghome=self.homedir, gpgbinary=self.binary)
		return _GPG(
            homedir=self.homedir, binary=self.binary, use_agent=True,
            keyring=self._keyring, secring=self._keyring)

	@staticmethod
	def __passwd(rpt=True):
		"""
		password questioning function
		"""
		msg = 'enter the passphrase for your gpg-key:'
		tru = 'repeat that passphrase:'
		while True:
			try:
				if not rpt:
					return _getpass(msg)
				__pwd = _getpass(msg)
				if __pwd == _getpass(tru):
					return __pwd
				error('passwords did not match')
			except KeyboardInterrupt:
				abort()

	def genkeys(self, **kginput):
		"""
		gpg-key-pair generator method
		"""
		if self.dbg:
			print(bgre(self.genkeys))
		kginput = kginput if kginput != {} else self.kginput
		if not kginput:
			error('no key-gen input received')
			return
		print(
            blu('generating new keys using:\n '),
            '\n  '.join('%s%s=  %s'%(
                blu(k),
                ' '*int(max(len(s) for s in kginput.keys())-len(k)+2),
                yel(v)
            ) for (k, v) in kginput.items()))
		if 'passphrase' in kginput.keys():
			if kginput['passphrase'] == 'nopw':
				del kginput['passphrase']
			elif kginput['passphrase'] == 'stdin':
				kginput['passphrase'] = self.__passwd()
		print(red('generating %s-bit keys - this WILL take some time'%(
            kginput['key_length'])))
		return self._gpg_.gen_key(self._gpg_.gen_key_input(**kginput))

	def export(self, pattern=None, privat=False, typ='a'):
		"""
		key-export method
		"""
		if self.dbg:
			print(bgre(self.export))
		pubs = []
		for keys in self._gpg_.list_keys():
			if pattern:
				if not [v for kv in keys.values() for v in kv if pattern in v]:
					continue
			for (key, val) in keys.items():
				#rint(key, val)
				if key == 'subkeys':
					for sub in keys[key]:
						finger, typs = sub
						if 'e' in typs:
							si = keys[key].index(sub)
							ki = keys[key][si].index(finger)
							pubs.append(
								self._gpg_.export_keys(keys[key][si][ki]))
		if pubs and len(pubs) == 1:
			return pubs[0]
		return pubs

	def _keystrencrypt(self, message, keystr):
		for result in self._gpg_.import_keys(keystr).results:
			finger = result['fingerprint']
			return self._gpg_.encrypt(
                message, finger, **{'always_trust': True})

	def encrypt(self, message, keystr=None):
		"""
		text encrypting function
		"""
		if self.dbg:
			print(bgre(self.encrypt))
		if keystr:
			return self._keystrencrypt(message, keystr)

	def decrypt(self, message):
		"""
		text decrypting function
		"""
		if self.dbg:
			print(bgre(self.decrypt))
		return self._gpg_.decrypt(str(message).encode(), always_trust=True)
