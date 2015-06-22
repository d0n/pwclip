#!/usr/bin/env python3
"""efibootmgr wrapping module"""
# global imports
import re
import os
import sys

# local relative imports
from colortext import error
from systools import which
from executor import Command

# default vars
__version__ = '0.1'

class UEFITool(Command):
	_sh_ = True
	_su_ = True
	_dbg = False
	_efimgrbin = which('efibootmgr')
	def __init__(self, *args):
		for arg in args:
			arg = '_%s'%(arg)
			if arg in self.__dict__.keys() and self.__dict__[arg]:
				setattr(self, arg, False)
			setattr(self, arg, True)
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # efimgrbin <str>
	def efimgrbin(self):
		return self._efimgrbin

	def __efiout(self):
		out = self.stdo('%s -v'%(self._efimgrbin))
		return out.split('\n') if out else None

	def _efihex(self, pattern):
		for line in self.__efiout():
			if '|' in pattern:
				fpat = pattern.split('|')[0]
				spat = pattern.split('|')[1]
				if fpat in line or spat in line:
					return str(line.split(' ')[0])[:8][4:]
			elif '&' in pattern:
				fpat = pattern.split('&')[0]
				spat = pattern.split('&')[1]
				if fpat in line and spat in line:
					return str(line.split(' ')[0])[:8][4:]
			else:
				if pattern in line:
					return str(str(line.split(' ')[0])[-5:-1])
		raise RuntimeError(
		    'could not find %s in output of efibootmgr'%(pattern))

	def _efilabel(self, pattern):
		if self.efistatus == {}:
			self._efistat()
		efihex = self._efihex(pattern)
		return self.efistatus()['bootables'][efihex]['osname']

	def efistatus(self):
		status = {}
		bootables = {}
		for line in self.__efiout():
			if line.startswith('BootNext:'):
				status['next'] = line.split(' ')[1]
			elif line.startswith('BootCurrent:'):
				status['current'] = line.split(' ')[1]
			elif line.startswith('BootOrder:'):
				status['order'] = line.split(' ')[1]
			elif line.startswith('Timeout:'):
				status['timeout'] = line.split(' ')[1]
			elif line.startswith('Boot'):
				number = str(line.split(' ')[0])[:8][4:]
				osname = ' '.join(
				    str(line.split('\t')[0]).split(' ')[1:]).strip()
				target = re.sub(
				    '.*(File|HD|BIOS)\((.*)\).*', '\\2',
				    str(line.split('\t')[1]))
				bootables[number] = dict(
				    [('osname',osname), ('target',target)])
		status['bootables'] = dict(bootables)
		self._efistatus = status
		return status

	def nextboot(self, efihex=None):
		if efihex:
			if self.erno('%s -n %s' %(self.efimgrbin, efihex)) == 1:
				return True
		else:
			return self.stat()['next']









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(m for m in dir()))
