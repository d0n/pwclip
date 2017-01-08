#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""password list parsing library"""
# (std)lib imports
from os.path import \
    isdir as _isdir, \
    isfile as _isfile, \
    dirname as _dirname, \
    basename as _basename, \
    expanduser as _expanduser

from colortext import bgre, tabd


class PasswordListParser(dict):
	dbg = False
	usrpwds = {}
	def __init__(self, usrpwds):
		if self.dbg:
			print(bgre(PasswordListParser.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property                # usrpwds <dict>
	def usrpwds(self):
		return self._usrpwds

	def search(self, pattern):
		for (usr, pwd) in self.usrpwds.items():
			if pattern in usr:
				yield pwd
			elif pattern in pwd:
				yield usr



