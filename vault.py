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

from shutil import rmtree, move, copyfile

from yaml import load, dump

from secrecy import GPGTool

class WeakVaulter(GPGTool):
	home = expanduser('~')
	vault = '%s/.crypt'%home
	weakz = '%s/.weaknez'%home
	recvs = []
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	def __init__(self):
		self._clean_()

	def _fixmod_(self):
		try:
			chmod('%s/.gnupg'%self.home, 0o700)
		except FileNotFoundError:
			pass

	def _clean_(self):
		self._fixmod_()
		for ln in listdir(self.home):
			ln = '%s/%s'%(self.home, ln)
			if islink(ln) and not isdir(readlink(ln)):
				remove(ln)
			if not islink(ln) and isdir('%s.1'%ln):
				move('%s.1'%ln, ln)

	def _pathdict(self, path):
		frbs = {}
		for (d, _, fs) in walk(path):
			for f in fs:
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
				if not isdir('%s.1'%hl):
					move(hl)
				try:
					rmtree(hl)
				except FileNotFoundError:
					pass
			if isdir('%s.1'%hl):
				move('%s.1'%hl, hl)
			try:
				remove(ln)
			except (IsADirectoryError, FileNotFoundError):
				pass
		self._fixmod_()

	def _mklns_(self, weak):
		pwd = getcwd()
		chdir(self.home)
		whh = '%s/%s'%(basename(weak), uname()[1])
		for ln in ('.gnupg', '.ssh', '.vpn'):
			hl = '%s/%s'%(self.home, ln)
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
				symlink('%s/%s'%(whh, ln), ln)
			except FileExistsError:
				pass
		chdir(pwd)

	def envault(self):
		if not isdir(self.weakz):
			return
		copyfile(self.vault, '%s.1'%self.vault)
		self.encrypt(
            str(dump(self._pathdict(self.weakz))),
            output=self.vault, recipients=self.recvs)
		rmtree(self.weakz)
		self._rmlns_()

	def unvault(self):
		if not isfile(self.vault) or isdir(self.weakz):
			return
		with open(self.vault, 'r') as cfh:
			self._dictpath(load(str(self.decrypt(cfh.read()))))
		self._mklns_(self.weakz)


