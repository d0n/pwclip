#!/usr/bin/env python3
# global imports
import re
import os
import sys
import shutil
import difflib
# local relative imports

from .git import GitRepo
from lib.colortext import error
from lib.executor import Command
from lib.misc import whoami

# default vars
__version__ = '0.2'

class ConfigSyncer(GitRepo):
	"""
	config syncer is iterating over files in a known directory (or repo)
	and checks for differences of the files within against the ones found
	on the running system
	"""
	_dbg = False
	_dry = False
	_r2s = False
	_frc = False
	_iac = False
	user = whoami()
	repodir = os.path.expanduser('~/cfg')
	branchs = ['master', os.uname()[1]]
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%arg
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(ConfigSyncer.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, val, sep=' = ')
			print()

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property                # dry <bool>
	def dry(self):
		return self._dry
	@dry.setter
	def dry(self, val):
		self._dry = val if type(val) is bool else self._dry
	@property                # r2s <bool>
	def r2s(self):
		return self._r2s
	@r2s.setter
	def r2s(self, val):
		self._r2s = val if type(val) is bool else self._r2s
	@property                # iac <bool>
	def iac(self):
		return self._iac
	@iac.setter
	def iac(self, val):
		self._iac = val if type(val) is bool else self._iac
	@property                # frc <bool>
	def frc(self):
		return self._frc
	@frc.setter
	def frc(self, val):
		self._frc = val if type(val) is bool else self._frc

	def __delpat(self, rpofile):
		return re.sub('USER', self.user, re.sub(self.repodir, '', rpofile))

	def __deref(self, srcfile, trgfile):
		if os.path.islink(srcfile):
			if not os.path.islink(trgfile):
				if os.path.isfile(trgfile):
					os.remove(trgfile)
				os.chdir(os.path.dirname(trgfile))
				os.symlink(os.readlink(srcfile), os.path.basename(srcfile))
			srcfile = os.readlink(srcfile)
			trgfile = '%s%s' %(self.repodir, srcfile)
		return srcfile, trgfile

	def __diff(self, srcfile, trgfile):
		if (os.path.isfile(srcfile) and os.path.isfile(trgfile) and
	          os.access(srcfile, os.R_OK) and os.access(trgfile, os.R_OK)):
			try:
				with open(srcfile, 'r') as srf, open(trgfile, 'r') as trf:
					src = srf.readlines()
					trg = trf.readlines()
			except (UnicodeDecodeError, PermissionError):
				return False
			diff = [
                d.strip() for d in difflib.ndiff(src, trg) if (d and
                    d.startswith('+ ') or d.startswith('- '))
                ]
			if diff:
				return diff

	def __stampcomp(self, sysfile, repofile):
		sysstamp = 0
		rpostamp = self.commitstamp(repofile)
		if os.path.exists(sysfile) and os.access(sysfile, os.R_OK):
			sysstamp = int(os.stat(sysfile).st_mtime)
		if rpostamp and rpostamp > sysstamp:
			return repofile, sysfile
		return sysfile, repofile

	def __stats(self, f):
		if os.path.isfile(f):
			return {
                'uid':os.stat(f).st_uid,
                'gid':os.stat(f).st_gid,
                'mod':os.stat(f).st_mode
                }

	def __copy(self, src, trg, stat):
		if not os.path.isdir(os.path.dirname(trg)):
			try:
				os.makedirs(os.path.dirname(trg))
			except PermissionError as err:
				if self.dbg:
					error(err)
				return False
		try:
			shutil.copy2(src, trg)
		except PermissionError as err:
			if self.dbg:
				error(err)
			return False
		return True

	def __mklink(self, sysfile, rpofile):
		if self.r2s:
			sysfile, rpofile = rpofile, sysfile
		if os.path.islink(rpofile):
			lcwd = os.getcwd()
			try:
				os.chdir(os.path.dirname(sysfile))
				os.symlink(sysfile, os.readlink(rpofile))
			except PermissionError as err:
				if self.dbg:
					error(err)
			finally:
				os.chdir(lcwd)
			return True

	def __dialog(self, srcfile, trgfile, stat):
		yesno = input('overriding:\n  %s => %s [%s]\n\nare you sure? [Y/n]'%(
            srcfile, trgfile, stat))
		if not yesno.lower() == 'n':
			return True

	def sync(self, branchs=None):
		if self.dbg:
			print(self.sync)
			print('mode =', 'rpo2sys' if self.r2s else 'sys2rpo')
		if not branchs:
			branchs = self.branchs
		os.chdir(self.repodir)
		if not self._gitdir():
			raise RuntimeError(
                'not ".git" folder found in current path %s'%repodir)
		branchdiffs = {}
		for branch in branchs:
			filediffs = {}
			if self._head() != branch:
				self.checkout(branch)
			for (dirs, subs, files) in os.walk(self.repodir):
				if '.git' in dirs:
					continue
				for f in files:
					if f == '.gitignore':
						continue
					srcfile, trgfile = self.__deref(
                        self.__delpat('%s/%s' %(dirs, f)), '%s/%s' %(dirs, f))
					if self.r2s:
						srcfile, trgfile = '%s/%s'%(dirs, f), self.__delpat(
                            '%s/%s' %(dirs, f))
						diffs = self.__diff(trgfile, srcfile)
					if self.__mklink(srcfile, trgfile):
						continue
					stat = self.__stats(srcfile)
					if not self.r2s:
						if branch == 'master' and not self.frc:
							srcfile, trgfile = self.__stampcomp(
                                srcfile, trgfile)
						diffs = self.__diff(trgfile, srcfile)
						stat = self.__stats(trgfile)
					if not diffs: # and not self.frc:
						continue
					if not os.path.isfile(srcfile):
						if not self.frc:
							srcfile, trgfile = trgfile, srcfile

					if self.iac:
						print('\n===\n%s\n==='%'\n'.join(diff for diff in diffs))
						self.__dialog(srcfile, trgfile, stat)
					if diffs:
						self.__copy(srcfile, trgfile, stat)
						filediffs[trgfile] = diffs
			if filediffs != {}:
				self.add()
				self.commit(self.gitstatus())
				self.push()
				branchdiffs[branch] = filediffs
		return branchdiffs




if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	#syscfg = ConfigSyncer(*('dbg', ), **{'repodir': os.path.expanduser('~/cfg')})
	#branchdiffs = syscfg.sync()
	#for branch in branchdiffs:
	#	print('%s:'%branch)
	#	for files in branchdiffs[branch]:
	#		print('\t%s:'%files)
	#		if branchdiffs[branch][files]:
	#			for diffs in branchdiffs[branch][files]:
	#				print('\t\t%s'%diffs)
