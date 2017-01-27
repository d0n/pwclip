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
    remove, readlink, environ, chmod

from os.path import \
    isdir, islink, isfile, \
    dirname, expanduser, exists, basename

from psutil import process_iter as piter

from shutil import rmtree, move, copyfile

from paramiko.ssh_exception import SSHException

from yaml import load, dump

from socket import gaierror

from colortext import blu, yel, bgre, tabd, error

from executor import command as cmd

from system.user import whoami

from net import SecureSHell

from secrecy.diryamlvault import DirYamlVault

class WeakVaulter(SecureSHell, DirYamlVault):
	dbg = None
	home = expanduser('~')
	user = whoami()
	host = uname()[1]
	recvs = []
	remote = ''
	reuser = user
	vault = '%s/.vault'%home
	weakz = '%s/.weaknez'%home
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
		SecureSHell.__init__(self, *args, **kwargs)
		args = list(args) + ['rmp']
		kwargs['plain'] = kwargs['weakz']
		DirYamlVault.__init__(self, *args, **kwargs)

	def _movesocks_(self, src, trg):
		if self.dbg:
			print(bgre(self._movesocks_))
		try:
			socks = ['random_seed'] + [
                f for f in listdir(src) if f.startswith('S')]
			for s in socks:
				move('%s/%s'%(src, s), '%s/%s'%(trg, s))
		except FileNotFoundError:
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
		elif isdir('%s/%s'%(self.weakz, self.host)):
			self._mklns_()
		if self.rem:
			self._copynews_()

	def _rmlns_(self):
		if self.dbg:
			print(bgre(self._rmlns_))
		for ln in self.__dirs:
			hl = '%s/%s'%(self.home, ln)

	def _mklns_(self):
		if self.dbg:
			print(bgre(self._mklns_))
		__pwd = getcwd()
		chdir(self.home)
		whh = '%s/%s'%(basename(self.weakz), uname()[1])
		for ln in self.__dirs:
			hl = '%s/%s'%(self.home, ln)
			whl = '%s/%s'%(whh, ln)
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
		self._movesocks_(
            '%s/%s/.gnupg'%(self.weakz, uname()[1]), '%s/.gnupg.1'%self.home)
		chg = self.envault()
		self._rmlns_()
		if chg:
			self._copynews_()

	def weakvault(self):
		if self.dbg:
			print(bgre(self.weakvault))
		if not isfile(self.vault):
			return error(
                'vault ', self.vault, ' does not exist or is inaccessable')
		if exists(self.weakz):
			return
		self.unvault()
		self._movesocks_(
            '%s/.gnupg.1'%self.home, '%s/%s/.gnupg'%(self.weakz, uname()[1]))
		self._mklns_()
