#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#

from sys import stderr

from os import symlink, getcwd, listdir, \
     makedirs, walk, uname, chdir, remove, readlink, environ, chmod

from os.path import isdir, islink, isfile, dirname, expanduser, basename

from psutil import process_iter as piter

from shutil import rmtree, move, copyfile

from paramiko.ssh_exception import SSHException

from yaml import load, dump

from socket import gaierror

from colortext import bgre, blu, yel, error

from executor import command as cmd

from system.user import whoami

from net import SecureSHell as SSH

from secrecy import GPGTool

class WeakVaulter(SSH, GPGTool):
	_dbg = None
	_pwd = getcwd()
	rem = None
	home = expanduser('~')
	user = whoami()
	host = uname()[1]
	vault = '%s/.vault'%home
	weakz = '%s/.weaknez'%home
	stamp = '%s.stamp'%vault
	recvs = []
	remote = ''
	reuser = user
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	chdir(home)
	def __init__(self, *args, **kwargs):
		skwargs = kwargs
		if 'remote' in kwargs.keys():
			skwargs['host'] = kwargs['remote']
		if 'reuser' in kwargs.keys():
			skwargs['user'] = kwargs['reuser']
		SSH.__init__(self, *args, **skwargs)
		GPGTool.__init__(self, *args, **kwargs)
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '_%s'%(arg)):
				setattr(self, '_%s'%(arg), True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '_%s'%(key)):
				setattr(self, '_%s'%(key), val)
		if '@' in self.remote:
			self.reuser, self.remote = self.remote.split('@')
		if self.rem:
			self._copynews_()
		self._clean_()
		if self.dbg:
			lim = int(max(len(k) for k in WeakVaulter.__dict__.keys()))+4
			print(bgre('%s\n%s\n\n%s\n%s\n'%(
                WeakVaulter.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(WeakVaulter.__dict__.items())),
                WeakVaulter.__init__,
                '\n'.join('  %s%s=    %s'%(k, ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items())))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	def _fixmod_(self):
		if self.dbg:
			print(bgre(self._fixmod_))
		for p in ('~/.gnupg', '~/.weaknez'):
			for (d, _, fs) in walk(expanduser(p)):
				for f in fs:
					if f.startswith('S.'):
						continue
					f = '%s/%s'%(d, f)
					#print(f)
					chmod(f, 0o600)
				#print(d)
				chmod(d, 0o700)

	def _movesocks_(self, src, trg):
		if self.dbg:
			print(bgre(self._movesocks_))
		socks = [
            f for f in listdir(src) if f.startswith('S')]
		socks.append('random_seed')
		for s in socks:
			try:
				move('%s/%s'%(src, s), '%s/%s'%(trg, s))
			except FileNotFoundError:
				pass

	def _copynews_(self):
		if self.rem and self.remote:
			try:
				self.scpcompstats(
                    self.vault, basename(self.vault), self.remote, self.reuser)
			except FileNotFoundError:
				pass

	def _clean_(self):
		if self.dbg:
			print(bgre(self._clean_))
		self._fixmod_()
		if not isdir(self.weakz):
			for ln in listdir(self.home):
				if not ln.startswith('.'):
					continue
				ln = '%s/%s'%(self.home, ln)
				if islink(ln) and not isdir(readlink(ln)):
					remove(ln)
					if isdir('%s.1'%ln):
						move('%s.1'%ln, ln)
				elif isdir(ln) and ln.endswith('.1') and \
                      not isdir(ln.rstrip('.1')):
					move(ln, ln.rstrip('.1'))
		elif isdir('%s/%s'%(self.weakz, self.host)):
			pwd = getcwd()
			chdir(self.home)
			whh = '%s/%s'%(basename(self.weakz), self.host)
			for ln in listdir(whh):
				hl = '%s/%s'%(self.home, ln)
				if not islink(hl) and isdir('%s/%s/%s'%(self.home, whh, ln)):
					if isdir(hl) and not isdir('%s.1'%hl):
						move(hl, '%s.1'%hl)
					elif isdir('%s.1'%hl):
						remove('%s.1'%hl)
					symlink('%s/%s'%(whh, ln), ln)
			chdir(pwd)

	def _pathdict(self, path):
		if self.dbg:
			print(bgre(self._pathdict))
		chdir(self.home)
		frbs = {}
		for (d, _, fs) in walk(path):
			for f in fs:
				if f == 'random_seed':
					continue
				f = '%s/%s'%(d, f)
				try:
					with open(f, 'rb') as rbf:
						rb = rbf.read()
					frbs[f] = rb
				except OSError:
					pass
		return frbs

	def _dictpath(self, dic):
		if self.dbg:
			print(bgre(self._dictpath))
		if not dic:
			return error('cannot decrypt')
		for (f, b) in dic.items():
			if not isdir(dirname(f)):
				makedirs(dirname(f))
			try:
				with open(f, 'wb+') as fwh:
					fwh.write(b)
			except PermissionError:
				pass

	def _rmlns_(self):
		if self.dbg:
			print(bgre(self._rmlns_))
		for ln in ('.gnupg', '.ssh', '.vpn'):
			hl = '%s/%s'%(self.home, ln)
			try:
				remove(hl)
			except IsADirectoryError:
				if isdir('%s.1'%hl):
					rmtree(hl)
			except FileNotFoundError:
				pass
			if isdir('%s.1'%hl):
				move('%s.1'%hl, hl)
		self._fixmod_()

	def _mklns_(self, weak):
		if self.dbg:
			print(bgre(self._mklns_))
		whh = '%s/%s'%(basename(weak), uname()[1])
		for ln in ('.gnupg', '.ssh', '.vpn'):
			hl = '%s/%s'%(self.home, ln)
			whl = '%s/%s'%(whh, ln)
			try:
				isdir(readlink(readlink(hl)))
				continue
			except OSError:
				pass
			if isdir(hl) and not isdir('%s.1'%hl):
				move(hl, '%s.1'%hl)
			elif not islink(hl) and isdir(hl) and isdir('%s.1'%hl):
				rmtree(hl)
			try:
				if isdir(whl):
					symlink(whl, ln)
			except FileExistsError:
				pass

	def _checkdiff(self):
		if self.dbg:
			print(bgre(self._checkdiff))
		nvlt = self._pathdict(basename(self.weakz))
		try:
			with open(self.vault, 'r') as cfh:
				ovlt = load(str(self.decrypt(cfh.read())))
		except FileNotFoundError:
			ovlt = False
		if ovlt != nvlt:
			return True

	def checkvault(self, vault):
		with open(vault, 'r') as vfh:
			vlt = vfh.readlines()
		if (
              vlt[0] == '-----BEGIN PGP MESSAGE-----\n' and \
              vlt[-1] == '-----END PGP MESSAGE-----\n'):
			return True

	def envault(self):
		if self.dbg:
			print(bgre(self.envault))
		if not isdir(self.weakz):
			return
		if self._checkdiff():
			try:
				copyfile(self.vault, '%s.1'%self.vault)
				chmod('%s.1'%self.vault, 0o600)
			except FileNotFoundError:
				pass
			self.encrypt(
                str(dump(self._pathdict(basename(self.weakz)))),
                output=self.vault, recipients=self.recvs)
		try:
			self._movesocks_(
                '%s/%s/.gnupg'%(self.weakz, self.host),
                '%s/.gnupg.1'%self.home)
		except FileNotFoundError:
			pass
		if self.checkvault(self.vault):	
			rmtree(self.weakz)
			self._rmlns_()
			chmod(self.vault, 0o600)
		chdir(self._pwd)
		if self.rem:
			self._copynews_()

	def unvault(self):
		if self.dbg:
			print(bgre(self.unvault))
		if not isfile(self.vault):
			error('vault', self.vault, 'does not exist or is inaccessable')
		elif isdir(self.weakz):
			return
		if self.weakz and isdir(dirname(self.weakz)):
			chdir(dirname(self.weakz))
		with open(self.vault, 'r') as cfh:
			try:
				dct = load(str(self.decrypt(cfh.read())))
			except RuntimeError:
				return
			if not dct:
				return
			self._dictpath(dct)
		self._mklns_(self.weakz)
		try:
			self._movesocks_(
                '%s/.gnupg.1'%self.home, '%s/%s/.gnupg'%(self.weakz, self.host))
		except (OSError, FileNotFoundError):
			pass
		self._fixmod_()
		chdir(self._pwd)

