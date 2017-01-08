#!/usr/bin/env python3
"""blkid wrapper tool for reading block devices"""
# global imports
import re
import os
import sys
import stat
from glob import glob
# local relative imports
from executor import Command
from system import absrelpath, which
from colortext import bgre, tabd
# default vars
__version__ = '0.1'

# os.statvfs(tst)
class BLocKIDs(Command):
	sh_ = True
	sieves=['DEVNO', 'PRI', 'TIME']
	_tab = {}
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
		blkfile = '/etc/blkid.tab'
		blkidbin = which('blkid')
		if not os.path.isfile(blkfile):
			self.su = True
			err = self.erno(blkidbin)
			if err != 0:
				print(
				    'executing blkid returned code',
				    err, file=sys.stderr)
		with open(blkfile, 'r') as blk:
			blkid = [
			    line.strip() for line in blk.readlines() if line.strip()]
		devinfos = {}
		for line in blkid:
			lindev = re.sub(
			    '<device (.*)>(.*)</device>$', '\\1;\\2', line)
			line, dev = lindev.split(';')
			devinfos[dev] = dict(
			    keyval.split('=') for keyval in line.split(' ')
			    )
		return  devinfos

	def _disks(self):
		disks = []
		for dev in os.listdir('/dev'):
			dev = '/dev/%s'%(dev)
			if os.stat(dev).st_gid == 6 and not dev[-1].isdigit():
				disks.append(dev)
		for dev in os.listdir('/dev/mapper'):
			dev = '/dev/mapper/%s'%(dev)
			if os.stat(dev).st_gid == 6 and not os.path.islink(dev):
				disks.append(dev)
		return disks

	def _mappings(self):
		mappdir = '/dev/mapper'
		mappings = {}
		for mapping in os.listdir(mappdir):
			if mapping == 'control':
				continue
			mapping = '%s/%s' %(mappdir, mapping)
			if os.path.islink(mapping):
				mappings[os.path.abspath(os.readlink(mapping))] = mapping
			else:
				mappings[mapping] = mapping
		return mappings

	def _disklabels(self):
		labeldir = '/dev/disk/by-label'
		dsklbls = {}
		for label in os.listdir(labeldir):
			dsklbls[label] = absrelpath(
			    '%s/%s'%(labeldir, label), base=labeldir)
		return dsklbls

	def _fstab(self, entry=''):
		fstab = '/etc/fstab'
		with open(fstab , 'r') as tab:
			return [t for t in tab.readlines() if t and entry in t]

	def typeval(self, pattern):
		# dev, par, mnt, trg, img, err
		try:
			if pattern.isdigit() or float.fromhex(pattern):
				return 'err'
		except ValueError as err:
			pass
		path = absrelpath(pattern)
		if os.path.exists(path):
			if os.path.islink(path):
				path = os.readlink(path)
			if os.path.ismount(path):
				return 'mnt'
			if (os.path.isfile(path) and
			      os.stat(path).st_rdev == 0 and
			      os.stat(path).st_dev > 64000):
				return 'img'
		disks = self._disks()
		for disk in disks:
			if (pattern == disk or
			      os.path.basename(pattern) == os.path.basename(disk)):
				return 'dsk'
		parteval = []
		for (dev, block) in self.tab.items():
			vals = [val.strip('"') for val in block.values()]
			if pattern in dev or len([m for m in vals if pattern == m]) == 1:
				parteval.append(dev)
		if len(parteval) == 1:
			return 'par'
		return 'trg'

	def _search_blktab(self, pattern, sieves=None):
		devblocks = {}
		if not sieves:
			sieves = self.sieves
		for device in self.tab:
			for (key, val) in self.tab[device].items():
				if (pattern == device or pattern == os.path.basename(device)
					  or os.path.basename(pattern) == os.path.basename(
				        device)[:-1]
					  or pattern in val):
					devblocks[device] = dict((
					    key, val.strip('"')
					    ) for (key, val) in self.tab[
					        device].items(
					    ) if (key not in sieves
					        and not val in sieves)
					    )
		if devblocks != {}:
			return devblocks

	def search(self, pattern):
		disks = self._disks()
		for disk in disks:
			if (pattern == disk or
			      os.path.basename(pattern) == os.path.basename(disk)):
				return {disk: {'TYPE': 'disk'}}
		tabhits = self._search_blktab(pattern)
		if tabhits:
			return tabhits






if __name__ == '__main__':
	# by default my modules print all classes/definitions they own
	"""
	for func in dir(sys.modules[__name__]):
		if not '-v' in sys.argv:
			if str(func).startswith('__') or func == 'func':
				continue
		print(func)
		if func in sys.argv:
			print(dir(func))
			continue
	print()
	"""
	import binascii
	pattern = ''
	if len(sys.argv) > 1:
		pattern = sys.argv[1]
	blkid = BlockDevices()
	print(blkid.typeval(pattern))
	#print(blkid.tab)
	#pattern = ''
	#if len(sys.argv) > 1:
	#	pattern = sys.argv[1]
	#for (key, val) in sorted(blkid.tab.items()):
	#	print(key, val)
	#for (key, val) in sorted(blkid.search(pattern).items()):
	#	print(key, val)
	#print(blkid.typeval(pattern))
