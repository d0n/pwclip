






class FstabParser(object):
	_dbg = False
	tabmap = {
		1: 'device',
		2: 'mounto',
		3: 'fstype',
		4: 'ptions',
		5: 'dmp',
		6: 'pas',
	}
	_tfile = '/etc/fstab'
	_fstab = []
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

	@property                # fstab <list>
	def fstab(self):
		self._fstab = self._fstab if self._fstab else self.__tablist()
		return self._fstab

	@staticmethod
	def __tablist(tabfile='/etc/fstab'):
		with open(tabfile, 'r') as tab:
			return [[i.strip() for i in l.split()] for l in tab.readlines() if l and not l[0].startswith('#')]
	

	@staticmethod
	def __writetab(self, tablist):
		pass

