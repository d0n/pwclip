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
class FstabParser(object):
	fstab = '/etc/fstab'
	_fslist = []
	def __init__(self, fstab=None):
		fstab = fstab if fstab else self.fstab

	@staticmethod
	def _fslist_(fstab):
		with open(fstab, 'r') as ffs:
			fslines = [l.split() for l in ffs.readlines() if (
                  l.strip() and not l.startswith('#'))]
		return [{
            'device': device, 'mount': mount,
            'fstype': fstype, 'options': options, 'dmp': dmp, 'pas': pas
            } for (device, mount, fstype, options, dmp, pas) in fslines]

	@property                # fslist <list>
	def fslist(self):
		if not self._fslist:
			self._fslist = self._fslist_(self.fstab)
		return self._fslist

	def fsfind(self, pattern):
		for fsentry in self.fslist:
			if [v for v in fsentry.values() if pattern in v]:
				yield fsentry
