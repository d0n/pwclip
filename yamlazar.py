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
    dirname, expanduser, exists, basename, \
    join as pjoin

from shutil import rmtree, move

from yaml import load, dump

from colortext import blu, yel, bgre, tabd, error

from system import absrelpath, fileage, filerotate

from secrecy import GPGTool

class Yamlazar():
	""""Yamlazar"""
	dbg = None
	rmp = None
	path = getcwd()
	ymla = ''
	__dic = {}
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(Yamlazar.__mro__))
			print(bgre(tabd(Yamlazar.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))

	def path2dict(self, path):
		if self.dbg:
			print(bgre(self.path2dict))
		frbs = {}
		frbs['dirs'] = []
		frbs['links'] = []
		frbs['files'] = []
		if not isdir(path): return
		for (d, ss, fs) in walk(path):
			frbs['dirs'].append({d: stat(d)})
			for l in ss:
				l  = pjoin(d, l)
				if islink(l):
					frbs['links'].append({l: readlink(l)})
			for f in fs:
				if f == 'random_seed':
					continue
				f = pjoin(d, f)
				if islink(f):
					frbs['links'].append({f: readlink(f)})
					continue
				try:
					with open(f, 'rb') as rbf:
						rb = rbf.read()
					frbs['files'].append({f: [rb, stat(f)]})
				except OSError:
					pass
		return frbs

	def dict2path(self, dic):
		if self.dbg:
			print(bgre(self.dict2path))
		print(tabd(dic))

	def create(self, path, ymla=None):
		ymla = ymla if ymla else '%s.yla'%path
		with open(ymla, 'wb+') as yfh:
			yfh.write(str(dump(self.path2dict(path))).encode())

	def extract(self, ymla, path=None):
		path = path if path else dirname(ymla)
		with open(ymla, 'rb') as yfh:
			self.dict2path(load(yfh.read()))
