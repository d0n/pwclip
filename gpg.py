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
	_gnupghome = _expanduser('~/.gnupg')
	_gpgbinary = '/usr/bin/gpg'
	if not _isfile(_gpgbinary):
		print(_gpgbinary)
		_gpgbinary = '/usr/bin/gpg2'
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

	@property                # gpgdir <str>
	def gnupghome(self):
		"""string"""
		return self._gnupghome
	@gnupghome.setter
	def gnupghome(self, val):
		self._gnupghome = _expanduser(val) if val.startswith('~') else val
		if not self._gnupghome.startswith('/'):
			self._gnupghome = '%s/%s'%(_getcwd(), val)

	@property                # gpgbin <str>
	def gpgbinary(self):
		"""string"""
		return self._gpgbinary
	@gpgbinary.setter
	def gpgbinary(self, val):
		if _isfile(val) and _access(val, _XOK):
			self._gpgbinary = val
		if not _isfile(self._gpgbinary) or not _access(self._gpgbinary, _XOK):
			raise RuntimeError('%s needs to be executable'%self._gpgbinary)

	@property                # _gpg_ <GPG>
	def _gpg_(self):
		"""object"""
		return _GPG(gnupghome=self.gnupghome, gpgbinary=self.gpgbinary)

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

	def genkeys(self, kginput=None):
		"""
		gpg-key-pair generator method
		"""
		if self.dbg:
			print(bgre(self.genkeys))
		kginput = kginput if kginput else self.kginput
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

	def export(self, pattern=None):
		"""
		key-export method
		"""
		if self.dbg:
			print(bgre(self.export))
		for keys in self._gpg_.list_keys():
			for key in keys.keys():
				if key == 'subkeys':
					for sub in keys[key]:
						finger, typs, subf = sub
						if 'e' in typs:
							si = keys[key].index(sub)
							ki = keys[key][si].index(finger)
							return self._gpg_.export_keys(keys[key][si][ki])

	def encrypt(self, message, keystr=None):
		"""
		text encrypting function
		"""
		if self.dbg:
			print(bgre(self.encrypt))
		for result in self._gpg_.import_keys(keystr).results:
			finger = result['fingerprint']
			for key in self._gpg_.list_keys():
				if str(key['fingerprint']) == str(finger):
					mail = key['uids'][0].split(' ')[-1].strip('<>')
					crypt = self._gpg_.encrypt(
                        message, mail, **{'always_trust': True})
					if crypt:
						return crypt

	def decrypt(self, message):
		"""
		text decrypting function
		"""
		if self.dbg:
			print(bgre(self.decrypt))
		text = self._gpg_.decrypt(message.encode())
