#!/usr/bin/env python3
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
"""block device information gathering module"""

# global & stdlib imports
import re
import os
import sys

from stat import \
    S_ISBLK as _isblk

# local relative imports
from colortext import bgre, tabd
from system.sysfs import SysFs
from system import absrelpath

# global default variables
__version__ = '0.0'

class BlockDevice(object):
	_dbg = False
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(BlockDevice.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg

	def linkeds(self):
		devlnks = {}
		for (dirs, subs, files) in os.walk('/dev'):
			for dat in files:
				device = '%s/%s'%(dirs, dat)
				try:
					if (_isblk(os.stat(device).st_mode) and \
                          os.path.islink(device)):
						devlnks[device] = absrelpath(
                            os.readlink(device), base=os.path.dirname(device))
				except FileNotFoundError:
					pass
		return devlnks

	def devices(self):
		blkdevs = []
		for (dirs, subs, files) in os.walk('/dev'):
			for dat in files:
				device = '%s/%s'%(dirs, dat)
				try:
					if (_isblk(os.stat(device).st_mode) and not \
                          os.path.islink(device)):
						blkdevs.append(device)
				except FileNotFoundError:
					pass
		return sorted(blkdevs)



"""
	def hddsize(self, hdd, magic=1000.0):
		device = re.sub(r'\d$', '', hdd.split('/')[-1])
		sysfs = SysFs(os.path.realpath('/sys/block/%s'%device))
		print([f for f in sysfs.__iter__()])
		exit()
		sfs = self.sfs(os.path.realpath('/sys/block/%s'%device))
		ss = sfs.queue.hw_sector_size
		if device != hdd:
			sfs = SysFs('/sys/block/%s/%s'%(device, hdd))
		ns = sfs.size
		magic = float(magic)
		return (float(ns)*float(ss))/(magic*magic*magic)

	def fsusage(self, hdd, magic=1000.0):
		if not hdd.startswith('/dev'):
			if os.path.exists('/dev/%s'%hdd):
				hdd = '/dev/%s'%hdd
			elif os.path.exists('/dev/mapper/%s'%hdd):
				hdd = os.readlink('/dev/mapper/%s'%hdd)
			elif os.path.exists('/dev/mapper/'):
				for mapped in os.listdir('/dev/mapper'):
					if (hdd in mapped or 
					      hdd == os.path.basename(os.readlink(mapped))):
						hdd = os.readlink('/dev/mapper/%s'%mapped)
		return float(os.statvfs(hdd).f_bfree)/(magic*magic*magic)
"""






if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	blkid = BlockDevices()
	print(blkid.hddsize('/dev/sda2'))
