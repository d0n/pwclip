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

from os import symlink, getcwd, listdir, \
     makedirs, walk, uname, chdir, remove, readlink, environ, chmod

from os.path import isdir, islink, isfile, dirname, expanduser, basename

from psutil import process_iter as piter

from shutil import rmtree, move, copyfile

from paramiko.ssh_exception import SSHException

from yaml import load, dump

from executor import command as cmd

from net import SecureSHell as SSH

from colortext import bgre, blu, yel

from secrecy import GPGTool

class WeakVaulter(GPGTool):
	_dbg = None
	home = expanduser('~')
	user = environ['USER']
	host = uname()[1]
	vault = '%s/.vault'%home
	weakz = '%s/.weaknez'%home
	recvs = []
	remote = ''
	reuser = user
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	def __init__(self, *args, **kwargs):
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
		socks = [
            f for f in listdir(src) if f.startswith('S')]
		socks.append('random_seed')
		for s in socks:
			try:
				move('%s/%s'%(src, s), '%s/%s'%(trg, s))
			except FileNotFoundError:
				pass

	def _copynews_(self):
		if self.remote:
			ssh = SSH(host=self.remote, user=self.reuser)
			srctrg = ssh.compstats(basename(self.vault), basename(self.vault))
			if srctrg:
				src, trg = srctrg
				print('%s\n  %s %s %s'%(
                    blu('syncing more recent file:'),
                    yel(src), blu('=>'), yel(trg)))
				ssh.scpcompstats(basename(self.vault), basename(self.vault))

	def _clean_(self):
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
						rmtree(hl)
					symlink('%s/%s'%(whh, ln), ln)
			chdir(pwd)

	def _pathdict(self, path):
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
		if not dic:
			return
		for (f, b) in dic.items():
			if not isdir(dirname(f)):
				makedirs(dirname(f))
			try:
				with open(f, 'wb+') as fwh:
					fwh.write(b)
			except PermissionError:
				pass

	def _rmlns_(self):
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
		nvlt = self._pathdict(basename(self.weakz))
		with open(self.vault, 'r') as cfh:
			ovlt = load(str(self.decrypt(cfh.read())))
		if ovlt != nvlt:
			return True

	def envault(self):
		if not isdir(self.weakz):
			return
		__pwd = getcwd()
		chdir(expanduser('~'))
		if self._checkdiff():
			copyfile(self.vault, '%s.1'%self.vault)
			chmod('%s.1'%self.vault, 0o600)
			self._movesocks_(
                '%s/%s/.gnupg'%(self.weakz, self.host),
                '%s/.gnupg.1'%self.home)
			self.encrypt(
                str(dump(self._pathdict(basename(self.weakz)))),
                output=self.vault, recipients=self.recvs)
		rmtree(self.weakz)
		self._rmlns_()
		chmod(self.vault, 0o600)
		chdir(__pwd)

	def unvault(self):
		if not isfile(self.vault):
			error('vault', self.vault, 'does not exist or is inaccessable')
		elif isdir(self.weakz):
			return
		self._copynews_()
		__pwd = getcwd()
		chdir(expanduser('~'))
		with open(self.vault, 'r') as cfh:
			dct = load(str(self.decrypt(cfh.read())))
			if not dct:
				return error('could not decrypt')
			if dct == 'None':
				return
			elif dct:
				self._dictpath(dct)
		self._mklns_(self.weakz)
		self._movesocks_(
            '%s/.gnupg.1'%self.home, '%s/%s/.gnupg'%(self.weakz, self.host))
		self._fixmod_()
		chdir(__pwd)

