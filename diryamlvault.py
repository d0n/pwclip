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
    makedirs, symlink, walk, uname, chdir, \
    remove, readlink, environ, chmod, stat, utime

from os.path import \
    abspath, isdir, islink, isfile, \
    dirname, expanduser, exists, basename, join as pjoin

from shutil import rmtree, move

from yaml import load, dump

from colortext import blu, yel, bgre, tabd, error

from system import absrelpath, fileage, filerotate

from secrecy.gpgtools import GPGTool

class DirYamlVault(GPGTool):
	dbg = None
	age = 0
	path = ''
	vault = ''
	recvs = []
	force = False
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if not self.vault or not self.path:
			raise RuntimeError('setting a file and directory is mandatory')
		if not self.recvs:
			if 'GPGKEYS' in environ.keys():
				self.recvs = environ['GPGKEYS'].split(' ')
			elif 'GPGKEY' in environ.keys():
				self.recvs = [environ['GPGKEY']]
		self.path = absrelpath(self.path)
		self.vault = absrelpath(self.vault)
		self.age = stat(self.vault).st_atime
		if self.dbg:
			print(bgre(DirYamlVault.__mro__))
			print(bgre(tabd(DirYamlVault.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		GPGTool.__init__(self, *args, **kwargs)

	def _readvault(self):
		try:
			with open(self.vault, 'r') as vfh:
				plain = self.decrypt(vfh.read())
			recvs = [
                '0x%s'%l.split('[GNUPG:] ENC_TO ')[1].split(' ')[0] \
                for l in str(plain.stderr).split('\n') \
                if l.startswith('[GNUPG:] ENC_TO')]
			if recvs != self.recvs:
				self.force = True
			#print(plain)
			#print(dir(plain))
			return load(str(plain))
		except FileNotFoundError:
			pass

	def path2dict(self, path):
		if self.dbg:
			print(bgre(self.path2dict))
		frbs = {}
		if not isdir(path): return
		for (d, ss, fs) in walk(path):
			for l in ss:
				l  = pjoin(d, l)
				if islink(l):
					frbs['<%s>'%l] = readlink(l)
			for f in fs:
				if f == 'random_seed':
					continue
				f = pjoin(d, f)
				if islink(f):
					frbs['<%s>'%f] = readlink(f)
					continue
				try:
					with open(f, 'rb') as rbf:
						rb = rbf.read()
					frbs[f] = rb
				except OSError:
					pass
		return frbs

	def dict2path(self, dic):
		if self.dbg:
			print(bgre(self.dict2path))
		if not dic:
			return error('cannot decrypt')
		_pwd = getcwd()
		for (f, b) in dic.items():
			if f.startswith('<') and f.endswith('>'):
				f = f.strip('<>')
				if not isdir(dirname(f)):
					makedirs(dirname(f))
				chdir(dirname(f))
				symlink(b, basename(f))
				continue
			if not isdir(dirname(f)):
				makedirs(dirname(f))
			try:
				with open(f, 'wb+') as fwh:
					fwh.write(b)
			except OSError as err:
				error(err)
		chdir(_pwd)

	def envault(self):
		if self.dbg:
			print('%s\n%s\n%s'%(
                bgre(self.envault), bgre(self.path), bgre(self.vault)))
		nvlt = self.path2dict(self.path)
		isok = False
		try:
			ovlt = self._readvault()
			equal = (nvlt == ovlt)
		except (KeyboardInterrupt, PermissionError):
			equal = False
		if self.force or (nvlt and not equal):
			filerotate(self.vault, 2)
			isok = self.encrypt(str(dump(nvlt)), output=self.vault).ok
			chmod(self.vault, 0o600)
		rmtree(self.path)
		return isok

	def unvault(self):
		if self.dbg:
			print('%s\n%s\n%s'%(
                bgre(self.unvault), bgre(self.vault), bgre(self.path)))
		if not isdir(self.path):
			makedirs(self.path)
		self.dict2path(self._readvault())
