#!/usr/bin/env python3
"""blkid wrapper tool for reading block devices"""
# global imports
from os.path import isfile, ismount
from psutil import disk_partitions
# local relative imports
from executor import Command
from system import absrelpath, which
from colortext import bgre, tabd
# default vars
__version__ = '0.1'

# os.statvfs(tst)
class BlockDevice(Command):
	sh_ = True
	sieves=['DEVNO', 'PRI', 'TIME']
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(BlockDevices.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	# ro properties
	@property               # tab <dict>
	def tab(self):
		__tabs = {}
		for t in self.stdo('blkid').split('\n'):
			if not t: continue
			disk, ats = t.split(':')
			attrs = {}
			for a in ats.split('" '):
				attrs[a.split('="')[0].strip().lower()] = \
                    a.split('=')[1].strip('"')
			__tabs[disk] = attrs
		return  __tabs

	@property
	def mounts(self):
		__mnts = {}
		__psps = disk_partitions()
		for mnt in __psps:
			__mnts[mnt[0]] = {
                'path': mnt[1],
                'type': mnt[2],
                'opts': mnt[3]}
		return __mnts

	def trgtype(self, trg):
		# dsk, mnt, img
		if trg in self.tab.keys():
			return 'dsk'
		elif ismount(absrelpath(trg)):
			return 'mnt'
		elif isfile(absrelpath(trg)):
			return 'img'

	def dsksearch(self, pattern, mode='name'):
		hits = []
		for (dsk, attrs) in self.tab.items():
			pass





if __name__ == '__main__':
	exit(1)
