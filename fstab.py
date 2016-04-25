# -*- coding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
from colortext import fatal

class FstabParser(object):
	_dbg = False
	tabmap = {
        0: 'device',
        1: 'mounto',
        2: 'fstype',
        3: 'fsopts',
        4: 'dmp',
        5: 'pas',
    }
	fstab = '/etc/fstab'
	_tablist = []
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in FstabParser.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                FstabParser.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(FstabParser.__dict__.items())),
                FstabParser.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	@property                # tablist <list>
	def tablist(self):
		return self._tablist if self._tablist else self.__tablist(self.fstab)
	@tablist.setter          # tablist <list>
	def tablist(self, val):
		if not self.__istablist(val):
			raise ValueError(
                'value %s not processable, need list of lists'%val)
		self._tablist = val

	@staticmethod
	def __istablist(tablist):
		if max(max(list(len(i) for i in l) for l in tablist)) != 1:
			return True

	@staticmethod
	def __tablist(fstab='/etc/fstab'):
		with open(fstab, 'r') as tab:
			return [
                [i.strip() for i in l.split()
                ] for l in tab.readlines() if l and not l[0].startswith('#')]


	def writetab(self, tablist=[[]]):
		if not self.__istablist(tablist):
			fatal('cannot process', val, 'need list of lists', '[[]]')
		with open(self.fstab, 'w+') as fsh:
			fsh.write('\n'.join(' '.join(i for i in l) for l in self.tablist))


