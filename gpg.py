#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
gpgtool module
"""

# (std)lib imports
from os import X_OK, access, getcwd, environ, path, name as osname

from getpass import getpass

from psutil import process_iter as piter

from tkinter import TclError

from getpass import getpass

from gnupg import GPG

# local imports
from colortext import blu, red, yel, bgre, tabd, abort, error, fatal

from system import xinput, xyesno, xmsgok



class GPGTool(object):
	"""
	gnupg wrapper-wrapper :P
	although the gnupg module is quite handy and the functions are pretty and
	useable i need some modificated easing functions to be able to make the
	main code more easy to understand by wrapping multiple gnupg functions to
	one - also i can prepare some program related stuff in here
	"""
	_dbg = None
	homedir = path.join(path.expanduser('~'), '.gnupg')
	__bindir = '/usr/bin'
	__gpgbin = 'gpg2'
	if osname == 'nt':
		__bindir = 'C:\Program Files (x86)\GNU\GnuPG'
		__gpgbin = 'gpg2.exe'
	binary = path.join(__bindir, __gpgbin)
	if not path.isfile(binary) or not access(binary, X_OK):
		raise RuntimeError('%s needs to be executable'%binary)
	agentinfo = path.join(homedir, 'S.gpg-agent')
	kginput = {}
	__pin = None
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%arg
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
		self._dbg = bool(val)

	@property                # keyring <str>
	def keyring(self):
		__bin = self.binary.rstrip('.exe')
		return path.join(self.homedir, 'pubring.kbx') \
            if __bin.endswith('2') else path.join(self.homedir, 'pubring.gpg')

	@property                # secring <str>
	def secring(self):
		__bin = self.binary.rstrip('.exe')
		if __bin.endswith('2') and self.keyring.endswith('gpg'):
			return path.join(self.homedir, 'secring.gpg')
		elif not __bin.endswith('2'):
			return path.join(self.homedir, 'secring.gpg')
		return self.keyring

	@property                # _gpg_ <GPG>
	def _gpg_(self):
		"""object"""
		opts = ['--batch', '--always-trust']
		if osname != 'nt':
			opts.append('--pinentry-mode=loopback')
		if self.__pin: opts = opts + ['--passphrase=%s'%self.__pin]
		__g = GPG(
            keyring=self.keyring, secret_keyring=self.secring,
            gnupghome=self.homedir, gpgbinary=self.binary,
            use_agent=True, options=opts,
            verbose=1 if self.dbg else 0)
		__g.encoding = 'utf-8'
		return __g

	def _garr(self):
		for proc in piter():
			if proc.name() in ('gpg-agent', 'scdaemon', 'dirmngr'):
				try:
					proc.kill()
				except PermissionError:
					error(
                        'cannot kill process',
                        proc.name, 'with PID', proc.pid())
		gacfg = path.join(self.homedir, 'gpg-agent.conf')
		try:
			with open(gacfg, 'r') as afh:
				for l in afh.readlines():
					if 'enable-ssh-support' in l and not '#' in l:
						environ['GPG_AGENT_INFO'] = \
                            path.join(self.homedir, 'S.gpg-agent.ssh')
		except FileNotFoundError as err:
			error(err)
		environ['GPG_AGENT_INFO'] = path.join(self.homedir, 'S.gpg-agent')

	@staticmethod
	def _passwd(rpt=False):
		"""
		password questioning function
		"""
		msg = 'enter passphrase: '
		tru = 'repeat that passphrase: '
		while True:
			try:
				if not rpt:
					return getpass(msg)
				__pwd = getpass(msg)
				if __pwd == getpass(tru):
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
				kginput['passphrase'] = self.__passwd(rpt=True)
		print(red('generating %s-bit keys - this WILL take some time'%(
            kginput['key_length'])))
		key = self._gpg_.gen_key(self._gpg_.gen_key_input(**kginput))
		if self.dbg:
			print('key has been generated:\n%s'%str(key))
		return key

	@staticmethod
	def __find(pattern, *vals):
		for val in vals:
			if isinstance(val, (list, tuple)) and \
			      [v for v in val if pattern in v]:
				#print(val, pattern)
				return True
			elif pattern in val:
				#print(val, pattern)
				return True

	def findkey(self, pattern='', **kwargs):
		typ = 'A' if not 'typ' in kwargs.keys() else kwargs['typ']
		secret = False if not 'secret' in kwargs.keys() else kwargs['secret']
		keys = {}
		pattern = pattern if not pattern.startswith('0x') else pattern[2:]
		for key in self._gpg_.list_keys():
			if pattern and not self.__find(pattern, *key.values()):
				continue
			for (k, v) in key.items():
				#print(k, v)
				if k == 'subkeys':
					#print(k)
					for sub in key[k]:
						#print(sub)
						short, typs, finger = sub
						#print(finger, typs)
						if typ == 'A' or (typ in typs):
							si = key[k].index(sub)
							ki = key[k][si].index(finger)
							kstr = self._gpg_.export_keys(
                                key[k][si][ki], secret=secret)
							#print(kstr)
							keys[finger] = {typs: kstr}
		return keys

	def export(self, *patterns, **kwargs):
		"""
		key-export method
		"""
		if self.dbg:
			print(bgre(self.export))
		typ = 'A' if not 'typ' in kwargs.keys() else kwargs['typ']
		secret = False if not 'secret' in kwargs.keys() else kwargs['secret']
		keys = dict((k, v) for (k, v) in self.findkey(**kwargs).items())
		if patterns:
			keys = dict((k, v) for p in list(patterns) \
                for (k, v) in self.findkey(p, **kwargs).items())
		return keys

	def _encryptwithkeystr(self, message, keystr, output):
		fingers = [
            r['fingerprint'] for r in self._gpg_.import_keys(keystr).results]
		return self._gpg_.encrypt(
            message, fingers, always_trust=True, output=output)

	def encrypt(self, message, *args, **kwargs):
		"""
		text encrypting function
		"""
		if self.dbg:
			print(bgre(self.encrypt))
		fingers = list(self.export(**{'typ': 'e'}))
		if 'recipients' in kwargs.keys():
			fingers = list(self.export(*kwargs['recipients'], **{'typ': 'e'}))
		if 'keystr' in kwargs.keys():
			res = self._gpg_.import_keys(keystr).results[0]
			fingers = [res['fingerprint']]
		output = None if not 'output' in kwargs.keys() else kwargs['output']
		#print(fingers)
		return self._gpg_.encrypt(
            message, fingers, always_trust=True, output=output)

	def decrypt(self, message, output=None):
		"""
		text decrypting function
		"""
		if self.dbg:
			print(bgre('%s\n  trying to decrypt:\n%s'%(self.decrypt, message)))
		c = 0
		try:
			while True:
				__plain = self._gpg_.decrypt(
					message.strip(), always_trust=True, output=output)
				if __plain:
					return __plain
				if not __plain and c == 0:
					self._garr()
				if c > 3:
					try:
						xmsgok('too many wrong attempts')
					except TclError:
						input('too many wrong attempts')
					break
				elif c > 1 and c < 3:
					try:
						yesno = xyesno(
						  'decryption failed - try again?')
					except TclError:
						yesno = input(
							'no passphrase or no secret key, retry? [Y/n] ')
					if not yesno or yesno is not True and yesno.lower() == 'n':
						break
				elif c > 1 and not self.__pin:
					try:
						yesno = xyesno('no passphrase entered, retry?')
					except TclError:
						yesno = input(
							'no passphrase entered, retry? [Y/n] ')
					if yesno is False or yesno.lower() == 'n':
						break
				c+=1
				try:
					self.__pin = xinput('enter gpg-passphrase')
				except TclError:
					self.__pin = getpass('enter gpg-passphrase: ')
		except KeyboardInterrupt:
			pass
