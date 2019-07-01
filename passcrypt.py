#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""passcrypt module"""

from sys import argv, stdout

from os import path, remove, environ, chmod, stat, makedirs

import socket

from time import time

from yaml import load, dump, FullLoader

from paramiko.ssh_exception import SSHException

from colortext import blu, yel, grn, bgre, tabd, error

from system import \
    userfind, filerotate, setfiletime, \
    xgetpass, xmsgok, xinput, xnotify, \
    filetime, absrelpath, xyesno, random, copy

from net.ssh import SecureSHell

from secrecy.gpgtools import GPGTool, GPGSMTool, DecryptError, SignatureError

from atexit import register

class PassCrypt(GPGTool, SecureSHell):
	"""passcrypt main class"""
	dbg = None
	vrb = None
	aal = None
	fsy = None
	sho = None
	rem = None
	rnd = None
	out = None
	gsm = None
	key = None
	sig = True
	gui = None
	chg = None
	syn = None
	try:
		user = userfind()
		home = userfind(user, 'home')
	except FileNotFoundError:
		user = environ['USERNAME']
		home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])
	user = user if user else 'root'
	home = home if home else '/root'
	config = path.join(home, '.config', 'pwclip.cfg')
	plain = path.join(home, '.pwd.yaml')
	crypt = path.join(home, '.passcrypt')
	timefile = path.expanduser('~/.cache/PassCrypt.time')
	remote = ''
	reuser = user
	recvs = []
	key = ''
	keys = {}
	sslcrt = ''
	sslkey = ''
	sigerr = None
	genpwrex = None
	genpwlen = 24
	maxage = 3600
	__weaks = {}
	__oldweaks = {}
	def __init__(self, *args, **kwargs):
		"""passcrypt init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(PassCrypt.__mro__))
			print(bgre(tabd(PassCrypt.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		self.cpasmsg = '%s %s%s '%(
            blu('enter password for'), yel(self.crypt), blu(':'))
		gargs = list(args) + ['sig'] if self.sig else []
		if self.gui:
			gargs = list(args) + ['gui'] + ['sig'] if self.sig else []
			self.cpasmsg = 'enter password for %s: '%self.crypt
		if self.gsm or (
              self.gsm is None and self.recvs and [
                  r for r in self.recvs if r in GPGSMTool().keylist(True)]):
			GPGSMTool.__init__(self, *args, **kwargs)
		else:
			GPGTool.__init__(self, *args, **kwargs)
		self.keys = self.findkey()
		if not self.keys:
			self._mkconfkeys()
			SecureSHell.__init__(self, *args, **kwargs)
		if self._checktime():
			self._copynews()
		self.__weaks = self._readcrypt()
		self.__oldweaks = str(dict(sorted(self.__weaks.items())))
		self.__weaks = self._mergecrypt(self.__weaks)
		register(self._cryptpass)

	def __del__(self):
		self._cryptpass()

	def _cryptpass(self):
		chgs = []
		crecvs = []
		if path.isfile(self.crypt):
			erecvs = list(set(self.recvlist(self.crypt)))
			for r in erecvs:
				crecvs.append('0x%s'%r[-16:])
			for r in self.recvs:
				if r not in crecvs:
					chgs.append('+ %s'%r)
			for r in crecvs:
				if r not in self.recvs:
					chgs.append('- %s'%r)
		if self.__oldweaks != str(dict(sorted(self.__weaks.items()))) or chgs:
			msg = ('recipients have changed:\n',
                    '\n'.join(c for c in chgs),
                    '\nfrom:\n', ' '.join(erecvs),
                    '\nto:\n', ' '.join(self.recvs),
                    '\nencryption enforced...')
			if chgs:
				if not self.gui:
					error(*msg)
				else:
					xmsgok(' '.join(msg))
			if not self.recvs and not self.findkey():
				self.genkeys(self._gendefs(self.gui))
			if self.__weaks:
				if self._writecrypt(self.__weaks):
					try:
						self._copynews()
					except OSError:
						pass

	def _mkconfkeys(self):
		self.key = '0x%s'%str(self.genkeys())[-16:]
		cfgs = {'gpg': {}}
		override = False
		if path.isfile(self.config):
			override = True
			with open(self.config, 'r') as cfh:
				cfgs = dict(load(cfh.read(), Loader=Loader))
			if 'gpg' not in cfgs.keys():
				cfgs['gpg'] = {}
		cfgs['gpg']['key'] = self.key
		if 'recipients' not in cfgs['gpg'].keys():
			cfgs['gpg']['recipients'] = self.key
			self.recvs = [self.key]
		with open(self.config, 'w+') as cfh:
			cfh.write(str(dump(cfgs)))

	def _checktime(self):
		ok = True
		if self.maxage:
			tf = absrelpath(self.timefile)
			if not path.exists(path.dirname(tf)):
				makedirs(path.dirname(tf))
			now = int(time())
			if not path.exists(tf):
				with open(tf, 'w+') as tfh:
					tfh.write(str(now))
			with open(tf, 'r') as tfh:
				last = int(tfh.read())
			age = int(now-int(last))
			if age >= int(self.maxage):
				with open(tf, 'w+') as tfh:
					tfh.write(str(now))
				return True

	def _mergecrypt(self, __weaks):
		try:
			with open(self.plain, 'r') as pfh:
				__newweaks = load(pfh.read(), Loader=Loader)
			if not self.dbg:
				remove(self.plain)
		except FileNotFoundError:
			__newweaks = {}
		__newweaks = {} if not __newweaks else __newweaks
		for (su, ups) in __newweaks.items():
			for (usr, pwdcom) in ups.items():
				if su not in __weaks.keys():
					__weaks[su] = {}
				__weaks[su][usr] = pwdcom
		return __weaks

	def _copynews(self, force=None):
		"""copy new file method"""
		if self.dbg:
			print(bgre(self._copynews))
		if not self.rem:
			return
		if not self.remote:
			return
		if not self._checktime():
			return
		fs = (self.crypt,)
		if self.sig:
			fs = (self.crypt, '%s.sig'%self.crypt)
		isok = True
		for i in fs:
			ok = self.scpcompstats(
                i, path.basename(i),
                2, remote=self.remote, reuser=self.reuser)
			if ok:
				isok = True if ok and isok else False
				if self.gui:
					xnotify('file %s synced successfully'%path.basename(i))
				else:
					print(
                        blu('file'), yel(path.basename(i)),
                        blu('synced successfully'))
		return isok

	def _readcrypt(self):
		"""read crypt file method"""
		if self.dbg:
			print(bgre(self._readcrypt))
		__dct = {}
		try:
			__dct, err = self.decrypt(self.crypt)
		except DecryptError as err:
			error(err)
			exit(1)
		__dct = dict(load(str(__dct), Loader=FullLoader))
		if err:
			if err == 'SIGERR':
				if self.gui:
					yesno = xyesno('reencrypt, even though ' \
                        'the passcryt signature could not be verified?')
				else:
					print(grn('reencrypt, even though ' \
                        'the passcryt signature could not be verified?'),
                        '[Y/n]')
					yesno = input()
					yesno = True if yesno in ('', 'y') else False
				if yesno and __dct:
					self._writecrypt(__dct)
		return __dct

	def _writecrypt(self, __weaks):
		"""crypt file writing method"""
		if self.dbg:
			print(bgre(self._writecrypt))
		kwargs = {
            'output': self.crypt,
            'key': self.key,
            'recvs': self.recvs}
		isok = self.encrypt(message=dump(__weaks),  **kwargs)
		cfh = open(self.crypt, 'r')
		cfh.close()
		chmod(self.crypt, 0o600)
		now = int(time())
		setfiletime(self.crypt, (now, now))
		return isok

	def __askpwdcom(self, sysuser, usr, pwd, com, opw, ocom):
		if self.rnd:
			pwd = self.rndgetpass()
		if self.gui:
			if not pwd:
				pwd = xgetpass(
				    'as user %s: enter password for entry %s'%(sysuser, usr))
				pwd = pwd if pwd else opw
				if not pwd:
					xmsgok('password is needed if adding password')
					return
			if not com:
				com = xinput(
				    'enter comment (optional, "___" deletes the comment)')
			com = ocom if not com else com
			if com == '___':
				com = None
		else:
			if not pwd:
				print(blu('as user '), yel(sysuser), ': ', sep='')
				pwd = pwd if pwd else self.passwd(msg='%s%s%s%s: '%(
						blu('  enter '), yel('password '),
						blu('for entry '), yel('%s'%usr)))
				pwd = pwd if pwd else opw
				if not pwd:
					error('password is needed if adding password')
					return
			if not com:
				print(
                    blu('  enter '), yel('comment '),
                    blu('(optional, '), yel('___'),
                    blu(' deletes the comment)'), ': ', sep='', end='')
				com = input()
			com = ocom if not com else com
			if com == '___':
				com = None
		return [p for p in [pwd, com] if p is not None]

	def rndgetpass(self):
		while True:
			__pwd = random(self.genpwlen, self.genpwrex)
			yesno = False
			if self.gui:
				yesno = xyesno('use the following password: "%s"?'%__pwd)
			else:
				print('%s %s%s [Y/n]'%(
                    grn('use the following password:'),
                    yel(pwd), grn('?')), sep='')
				yesno = input()
				yesno = True if str(yesno).lower() in ('y', '') else False
			if yesno:
				break
		return __pwd

	def adpw(self, usr, pwd=None, com=None):
		"""password adding method"""
		if self.dbg:
			print(bgre(tabd({
                self.adpw: {'user': self.user, 'entry': usr,
                            'pwd': pwd, 'comment': com}})))
		if not self.aal:
			if self.user in self.__weaks.keys():
				if usr in self.__weaks[self.user]:
					if self.gui:
						xmsgok('entry %s already exists for user %s'%(
                            usr, self.user))
					else:
						error(
                            'entry', usr, 'already exists for user', self.user)
					return self.__weaks
				elif self.user not in self.__weaks.keys():
					self.__weaks[self.user] = {}
				try:
					__opw, __ocom = self.__weaks[self.user][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				pwdcom = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom)
				if pwdcom:
					self.__weaks[self.user][usr] = [p for p in pwdcom if p]
		else:
			for u in self.__weaks.keys():
				if usr in self.__weaks[u].keys():
					if self.gui:
						xmsgok('entry %s already exists for user %s'%(usr, u))
					else:
						error('entry', usr, 'already exists for user', u)
					continue
				try:
					__opw, __ocom = self.__weaks[u][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				pwdcom = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom)
				if pwdcom:
					self.__weaks[u][usr] = [p for p in pwdcom if p]
		return dict(self.__weaks)

	def chpw(self, usr, pwd=None, com=None):
		"""change existing password method"""
		if self.dbg:
			print(bgre(tabd({
                self.chpw: {'user': self.user, 'entry': usr, 'pwd': pwd}})))
		if not self.aal:
			if self.__weaks and self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				try:
					__opw, __ocom = self.__weaks[self.user][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				self.__weaks[self.user][usr] = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom)
			else:
				if self.gui:
					xmsgok('no entry named %s for user %s'%(usr, self.user))
				else:
					error('no entry named', usr, 'for user', self.user)
		else:
			for u in self.__weaks.keys():
				if usr not in self.__weaks[u].keys():
					if self.gui:
						xmsgok('entry %s does not exist for user %s'%(usr, u))
					else:
						error('entry', usr, 'does not exist for user', u)
					continue
				try:
					__opw, __ocom = self.__weaks[self.user][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				self.__weaks[u][usr] = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom)
		return dict(self.__weaks)

	def rmpw(self, usr):
		"""remove password method"""
		if self.dbg:
			print(bgre(tabd({self.rmpw: {'user': self.user, 'entry': usr}})))
		if self.aal:
			__w = dict(self.__weaks)
			for u in __w.keys():
				try:
					del self.__weaks[u][usr]
					setattr(self, 'chg', True)
				except KeyError:
					if self.gui:
						xmsgok('entry %s not found as user %s'%(usr, u))
					else:
						error('entry', usr, 'not found as user', u)
				if not self.__weaks[u].keys():
					del self.__weaks[u]
		else:
			if self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				del  self.__weaks[self.user][usr]
			else:
				if self.gui:
					xmsgok('entry %s not found as user %s'%(usr, self.user))
				else:
					error('entry', usr, 'not found as user', self.user)
			if self.user in self.__weaks.keys() \
                  and not self.__weaks[self.user].keys():
				del self.__weaks[self.user]
		return dict(self.__weaks)

	def lspw(self, usr=None, aal=None):
		"""password listing method"""
		if self.dbg and not self.gui:
			print(bgre(tabd({self.lspw: {'user': self.user, 'entry': usr}})))
		aal = True if aal else self.aal
		__ents = {}
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					usrs = [self.user] + \
                        [u for u in self.__weaks.keys() if u != self.user]
					for user in usrs:
						if user in self.__weaks.keys() and \
                              usr in self.__weaks[user].keys():
							__ents = {usr: self.__weaks[user][usr]}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr in __ents.keys():
					__ents = {usr: self.__weaks[self.user][usr]}
		return dict(__ents)

def lscrypt(usr, dbg=None):
	"""passlist wrapper function"""
	if dbg:
		print(bgre(lscrypt))
	__ents = {}
	if usr:
		__ents = PassCrypt().lspw(usr)
	return __ents




if __name__ == '__main__':
	exit(1)
