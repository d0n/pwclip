#!/usr/bin/env python3
"""efibootmgr wrapping module"""
# global imports
import re
import os
import sys

# local relative imports
from colortext import bgre, tabd, error
from system import which
from executor import Command

# default vars
__version__ = '0.1'


class UEFITool(Command):
	sh_ = True
	su_ = True
	dbg = False
	_efimgrbin = which('efibootmgr')
	__efiout_ = []
	def __init__(self, *args):
		for arg in args:
			print(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(UEFITool.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property               # efimgrbin <str>
	def efimgrbin(self):
		return self._efimgrbin

	@property                # _efiout <list>
	def _efiout_(self):
		if not self.__efiout_:
			self.__efiout_ = self.__efiout()
		return self.__efiout_

	def __efiout(self):
		out = self.stdo('%s -v'%(self._efimgrbin))
		if out:
			return out.split('\n')

	def _efihex(self, pattern):
		for line in self._efiout_:
			if '|' in pattern and '&' in pattern:
				fpat = pattern.split('&')[0]
				opats = [pattern.split('&')[1]]
				if '(' in opats[0]:
					opats = opats[0].strip('()').split('|')
				if fpat.lower() in line.lower() and [
                      h for h in opats if h.lower() in line.lower()]:
					return str(line.split(' ')[0])[:8][4:]
			elif '|' in pattern:
				fpat = pattern.split('|')[0]
				spat = pattern.split('|')[1]
				if (fpat.lower() in line.lower() or \
                      spat.lower() in line.lower()):
					return str(line.split(' ')[0])[:8][4:]
			elif '&' in pattern:
				fpat = pattern.split('&')[0]
				spat = pattern.split('&')[1]
				if (fpat.lower() in line.lower() and \
                      spat.lower() in line.lower()):
					return str(line.split(' ')[0])[:8][4:]
			else:
				if pattern.lower() in line.lower():
					return str(str(line.split(' ')[0])[-5:-1])
		raise RuntimeError(
            'could not find %s in output of efibootmgr'%(pattern))

	def _efilabel(self, pattern):
		efihex = self._efihex(pattern)
		return self.efistatus()['bootables'][efihex]['osname']

	def efistatus(self):
		status = {}
		bootables = {}
		for line in self._efiout_:
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
