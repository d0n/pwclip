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

from net import SecureSHell as SSH

from secrecy import GPGTool

class WeakVaulter(SSH, GPGTool):
	dbg = None
	rem = None
	nod = None
	nln = None
	home = expanduser('~')
	user = whoami()
	host = uname()[1]
	recvs = []
	remote = ''
	reuser = user
	_pwd = getcwd()
	_vault = '%s/.vault'%home
	_weakz = '%s/.weaknez'%home
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
		self._clean_()
		if self.dbg:
			print(bgre(WeakVaulter.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		SSH.__init__(self, *args, **kwargs)
		GPGTool.__init__(self, *args, **kwargs)

	@property                # weakz <str>
	def weakz(self):
		return self._abspath(self._weakz)
	@weakz.setter
	def weakz(self, val):
		self._weakz = val

	@property                # vault <str>
	def vault(self):
		return self._abspath(self._vault)
	@vault.setter
	def vault(self, val):
		self._vault = val

	@staticmethod
	def _abspath(path):
		if path.startswith('~'):
			path = expanduser(path)
		elif not path.startswith('/'):
			path = '%s/%s'%(getcwd(), path)
		return path

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
				chmod(d, 0o700)

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

	def _copynews(self):
		if self.dbg:
			print(bgre(self._copynews))
		if self.rem and self.remote:
			try:
				if self.scpcompstats(
                      self.vault, basename(self.vault),
                      self.remote, self.reuser):
					return True
			except FileNotFoundError:
				pass

	def _clean_(self):
		if self.dbg:
			print(bgre(self._clean_))
		if self.nod:
			return
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
			try:
				whh = '%s/%s'%(basename(self.weakz), self.host)
				for ln in listdir(whh):
					hl = '%s/%s'%(self.home, ln)
					if not islink(hl) and isdir('%s/%s/%s'%(self.home, whh, ln)):
						if isdir(hl) and not isdir('%s.1'%hl):
							move(hl, '%s.1'%hl)
						if isdir('%s.1'%hl) and isdir(hl) and not islink(hl):
							rmtree(hl)
						symlink('%s/%s'%(whh, ln), ln)
			finally:
				chdir(pwd)
		if self.rem:
			if self._copynews():
				self.unvault(force=True)

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
		if self.rem:
			self._copynews()

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
			if isdir(hl) and not isdir('%s.1'%hl) and not islink(hl):
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
		print(tabd(ovlt))
		print(tabd(nvlt))
		if ovlt != nvlt:
			return True

	def checkvault(self, vault):
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
			print(bgre(self.envault))
		if not exists(self.weakz):
			return
		try:
			if isdir(dirname(self.weakz)):
				chdir(dirname(self.weakz))
			if self._checkdiff():
				try:
					copyfile(self.vault, '%s.1'%self.vault)
					chmod('%s.1'%self.vault, 0o600)
				except FileNotFoundError:
					pass
				self.encrypt(
                    str(dump(self._pathdict(basename(self.weakz)))),
                    output=self.vault, recipients=self.recvs)
			if not self.nod and self.checkvault(self.vault):
				rmtree(self.weakz)
			if not self.nln:
				self._rmlns_()
				self._fixmod_()
				self._movesocks_(
                    '%s/%s/.gnupg'%(self.weakz, self.host),
                    '%s/.gnupg.1'%self.home)
			chmod(self.vault, 0o600)
		finally:
			chdir(self._pwd)

	def unvault(self, force=None):
		if self.dbg:
			print(bgre(self.unvault))
		if not isfile(self.vault):
			return error(
                'vault ', self.vault, ' does not exist or is inaccessable')
		try:
			with open(self.vault, 'r') as cfh:
				self._dictpath(load(str(self.decrypt(cfh.read()))))
			if not self.nln:
				self._mklns_(self.weakz)
				self._movesocks_(
                    '%s/.gnupg.1'%self.home,
                    '%s/%s/.gnupg'%(self.weakz, self.host))
				self._fixmod_()
		except (OSError, FileNotFoundError):
			pass
		finally:
			chdir(self._pwd)
