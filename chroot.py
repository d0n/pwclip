#/usr/bin/env python3
# -*- coding: utf-8 -*-
from .mounter import DeviceMounter

class ChangeRoot(object):
	_dbg = False
	_path = ''
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
			lim = int(max(len(k) for k in ChangeRoot.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                ChangeRoot.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(ChangeRoot.__dict__.items())),
                ChangeRoot.__init__,
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

	@property                # path <str>
	def path(self):
		return self._path
	@path.setter
	def path(self, val):
		self._path = val if isinstance(val, str) else self._path

	def run(self):
		pass
