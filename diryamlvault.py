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

from shutil import rmtree, move, copyfile

from yaml import load, dump

from colortext import blu, yel, bgre, tabd, error

from system import absrelpath

from secrecy import GPGTool

class DirYamlVault(GPGTool):
	dbg = None
	rmp = None
	recvs = []
	_vault = ''
	_plain = ''
	_pwd = getcwd()
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if not self.vault or not self.plain:
			raise RuntimeError('setting a file and directory is mandatory')
		if self.dbg:
			print(bgre(DirYamlVault.__mro__))
			print(bgre(tabd(DirYamlVault.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		GPGTool.__init__(self, *args, **kwargs)

	@property                # plain <str>
	def plain(self):
		return absrelpath(self._plain)
	@plain.setter
	def plain(self, val):
		self._plain = val

	@property                # vault <str>
	def vault(self):
		return absrelpath(self._vault)
	@vault.setter
	def vault(self, val):
		self._vault = val

	def _pathdict(self, path):
		if self.dbg:
			print(bgre(self._pathdict))
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

	def diffvault(self):
		if self.dbg:
			print(bgre(self.diffvault))
		nvlt = self._pathdict(basename(self.plain))
		try:
			with open(self.vault, 'r') as cfh:
				plain = self.decrypt(cfh.read())
				recvs = [
                    l.split('[GNUPG:] ENC_TO ')[1].split(' ')[0] \
                    for l in str(plain.stderr).split('\n') \
                    if l.startswith('[GNUPG:] ENC_TO')]
				srecvs = [
                    r.split('0x')[1] for r in self.recvs \
                    if r.startswith('0x')]
				if srecvs != recvs:
					return True
				ovlt = load(str(plain))
		except FileNotFoundError:
			return True
		if ovlt != nvlt:
			return True

	def checkvault(self, vault):
		if self.dbg:
			print(bgre(self.checkvault))
		try:
			with open(vault, 'r') as vfh:
				vlt = vfh.readlines()
			if (
                  vlt[0] == '-----BEGIN PGP MESSAGE-----\n' and \
                  vlt[-1] == '-----END PGP MESSAGE-----\n'):
				return True
		except FileNotFoundError:
			return False

	def envault(self):
		if self.dbg:
			print('%s\n%s\n%s'%(
                bgre(self.envault), bgre(self.plain), bgre(self.vault)))
		changed = False
		try:
			chdir(dirname(self.plain))
			if self.diffvault():
				changed = True
				try:
					copyfile(self.vault, '%s.1'%self.vault)
					chmod('%s.1'%self.vault, 0o600)
				except FileNotFoundError:
					pass
				self.encrypt(
                    str(dump(self._pathdict(basename(self.plain)))),
                    output=self.vault, recipients=self.recvs)
				chmod(self.vault, 0o600)
			if self.rmp:
				rmtree(self.plain)
		finally:
			chdir(self._pwd)
			return changed

	def unvault(self):
		if self.dbg:
			print('%s\n%s\n%s'%(
                bgre(self.unvault), bgre(self.vault), bgre(self.plain)))
		try:
			if not isdir(dirname(self.plain)):
				makedirs(dirname(self.plain))
			chdir(dirname(self.plain))
			with open(self.vault, 'r') as cfh:
				self._dictpath(load(str(self.decrypt(cfh.read()))))
		except (OSError, FileNotFoundError) as err:
			error('%s '%err,  self.vault, ' does not exist or is inaccessable')
		finally:
			chdir(self._pwd)
