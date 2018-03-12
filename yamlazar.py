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
    remove, readlink, environ, chown, chmod, stat, utime

from os.path import \
    abspath, isdir, islink, isfile, \
    dirname, expanduser, exists, basename, \
    join as pjoin

from pathlib import Path

from shutil import rmtree, move

from yaml import load, dump

from colortext import blu, yel, bgre, tabd, error

from system import absrelpath, fileage, filerotate

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

	def setmeta(self, path, metas):
		_m = metas
		try:
			chown(path, _m['uid'], _m['gid'])
		except PermissionError as err:
			print(error)
		chmod(path, _m['mod'])
		utime(path, (_m['atm'], _m['mtm']))

	def filemeta(self, path):
		""" uid, gid, mod, mtm, atm, ctm """
		s = list(stat(path))
		return {
            'uid': s[4], 'gid': s[5],
            'mod': s[0], 'mtm': s[7], 'atm': s[8]}
            #'st_uid': s[4], 'st_gid': s[5], 'st_mode': s[0],
            #'st_mtime': s[7], 'st_atime': s[8], 'st_ctime': s[9]}

	def path2dict(self, path):
		if self.dbg:
			print(bgre(self.path2dict))
		frbs = {}
		frbs['dirs'] = []
		frbs['links'] = []
		frbs['files'] = []
		if not isdir(path): return
		for (d, ss, fs) in walk(path):
			frbs['dirs'].append((d, self.filemeta(d)))
			for l in ss:
				l  = pjoin(d, l)
				if islink(l):
					frbs['links'].append((l, readlink(l)))
			for f in fs:
				if f == 'random_seed':
					continue
				f = pjoin(d, f)
				if islink(f):
					frbs['links'].append((f, readlink(f)))
					continue
				try:
					with open(f, 'rb') as rbf:
						rb = rbf.read()
					frbs['files'].append((f, rb, self.filemeta(f)))
				except OSError:
					pass
		return frbs

	def dict2path(self, dic):
		if self.dbg:
			print(bgre(self.dict2path))
		if not dic: return False
		dirs = dic['dirs']
		files = dic['files']
		links = dic['links']
		for dss in dirs:
			d, ss = dss
			try:
				makedirs(d)
			except FileExistsError:
				pass
			self.setmeta(d, ss)
		for fbs in files:
			f, b, s = fbs
			with open(f, 'wb+') as bfh:
				bfh.write(b)
		_pwd = getcwd()
		for lns in links:
			ln, trg = lns
			chdir(dirname(ln))
			symlink(ln, trg)
			chdir(_pwd)


	def create(self, path, ymla=None):
		ymla = ymla if ymla else '%s.yla'%path
		with open(ymla, 'wb+') as yfh:
			yfh.write(str(dump(self.path2dict(path))).encode())


	def extract(self, ymla, path=None):
		path = path if path else dirname(ymla)
		with open(ymla, 'rb') as yfh:
			self.dict2path(load(yfh.read()))
