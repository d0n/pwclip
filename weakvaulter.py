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

from os import \
    symlink, getcwd, listdir, \
    makedirs, walk, uname, chdir, \
    remove, readlink, environ, chmod, chown

from os.path import \
    isdir, islink, isfile, \
    dirname, expanduser, exists, \
    basename, join as pjoin

from psutil import process_iter as piter

from shutil import rmtree, move, copy2

from paramiko.ssh_exception import SSHException

from yaml import load, dump

from socket import gaierror

from colortext import blu, yel, bgre, tabd, error

from executor import command as cmd

from system.user import whoami

from net import SecureSHell

from secrecy.diryamlvault import DirYamlVault

class WeakVaulter(DirYamlVault, SecureSHell):
	dbg = None
	home = expanduser('~')
	user = whoami()
	host = uname()[1]
	recvs = []
	remote = ''
	reuser = user
	vault = pjoin(home, '.vault')
	weakz = pjoin(home, '.weaknez')
	__dirs = ['.gnupg', '.ssh', '.vpn']
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		self._clean_()
		if self.dbg:
			print(bgre(WeakVaulter.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		kwargs['plain'] = kwargs['weakz']
		SecureSHell.__init__(self, *args, **kwargs)
		DirYamlVault.__init__(self, *args, **kwargs)

	def _fixmod_(self):
		if self.dbg:
			print(bgre(self._fixmod_))
		fixmes = self.__dirs + [self.weakz]
		for p in fixmes:
			for (d, _, fs) in walk(expanduser(p)):
				for f in fs:
					if f.startswith('S.'):
						continue
					f = pjoin(d, f)
					#print(f)
					chmod(f, 0o600)
				#print(d)
				chmod(d, 0o700)
		for d in self.__dirs:
			try:
				chown(pjoin(self.home, d), 1000, 1000)
			except FileNotFoundError:
				pass

	def _mvrtfiles_(self, src, trg):
		if self.dbg:
			print(bgre(self._mvrtfiles_))
		rtfs = [f for f in listdir(src) if f and (
            f.startswith('S') or f.startswith('.#') or f == 'random_seed')]
		try:
			for s in rtfs:
				move(pjoin(src, s), pjoin(trg, s))
		except (FileNotFoundError, OSError):
			pass

	def _copynews_(self):
		if self.dbg:
			print(bgre(self._copynews_))
		if self.rem and self.remote:
			try:
				self.scpcompstats(
                      self.vault, basename(self.vault),
                      self.remote, self.reuser)
			except FileNotFoundError:
				pass

	def _clean_(self):
		if self.dbg:
			print(bgre(self._clean_))
		if not isdir(self.weakz):
			self._rmlns_()
		elif isdir(pjoin(self.weakz, self.host)):
			self._mklns_()
		self._fixmod_()
		if self.rem:
			self._copynews_()

	def _rmlns_(self):
		if self.dbg:
			print(bgre(self._rmlns_))
		for ln in self.__dirs:
			hl = pjoin(self.home, ln)
			try:
				remove(hl)
			except (IsADirectoryError, FileNotFoundError):
				continue
			try:
				move('%s.1'%hl, hl)
			except FileNotFoundError:
				pass

	def _mklns_(self):
		if self.dbg:
			print(bgre(self._mklns_))
		__pwd = getcwd()
		chdir(self.home)
		whh = pjoin(basename(self.weakz), uname()[1])
		for ln in self.__dirs:
			hl = pjoin(self.home, ln)
			whl = pjoin(whh, ln)
			if isfile(whl) or islink(hl):
				continue
			if not isdir('%s.1'%hl):
				try:
					move(hl, '%s.1'%hl)
				except FileNotFoundError:
					pass
			if isdir(hl) and isdir('%s.1'%hl):
				rmtree(hl)
			if not exists(hl):
				symlink(whl, ln)
		chdir(__pwd)

	def vaultweak(self):
		if self.dbg:
			print(bgre(self.vaultweak))
		if not exists(self.weakz):
			return
		try:
			self.envault()
		except ValueError as err:
			print(err)
		self._mvrtfiles_(
            pjoin(self.weakz, uname()[1], '.gnupg'),
            pjoin(self.home, '.gnupg.1'))
		try:
			rmtree(self.weakz)
		except FileNotFoundError:
			pass
		self._clean_()

	def weakvault(self, force=False):
		if self.dbg:
			print(bgre(self.weakvault))
		if not isfile(self.vault):
			return error(
                'vault ', self.vault, ' does not exist or is inaccessable')
		elif exists(self.weakz) and not force:
			return
		setattr(self, 'plain', dirname(self.weakz))
		self.unvault()
		self._mvrtfiles_(
            pjoin(self.home, '.gnupg.1'),
            pjoin(self.weakz, uname()[1], '.gnupg'))
		self._clean_()
