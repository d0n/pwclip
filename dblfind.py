#!/usr/bin/env python3
#
# This file is free software by  <- d0n - d0n@janeiskla.de ->
#
# You can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY! Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# Write to the Free Software Foundation, Inc.
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
""""dblfind iterates over files in a folder searing for equal files"""
# global imports
import os
import sys
import filecmp
# local relative imports
from system import absrelpath

def deldialog(src, trg):
	"""ask for file delete permission"""
	yesno = input('%s and %s seem to be the same file, delete one? [Y/n]'%(
        os.path.basename(src), os.path.basename(trg)))
	if yesno.lower() in ('y', ''):
		yesno = input('should %s be deleted? [Y/n]'%(
            os.path.basename(src))).strip()
		delfile = src
		if yesno not in ('y', ''):
			delfile = trg
			yesno = input('should %s be deleted? [Y/n]'%(
                os.path.basename(trg))).strip()
		if yesno.lower() in ('y', ''):
			os.remove(delfile)
			return delfile

def iterfiles(folder):
	"""iterate over files comparing them"""
	dels = []
	folder = absrelpath(folder)
	for (sdirs, _, sfiles) in os.walk(folder):
		for s in sfiles:
			for (tdirs, tsubs, tfiles) in os.walk(folder):
				for t in tfiles:
					if t == s:
						continue
					try:
						if filecmp.cmp(
                              '%s/%s'%(sdirs, s), '%s/%s'%(tdirs, t)):
							dels.append(
                                deldialog('%s/%s'%(
                                    sdirs, s), '%s/%s'%(tdirs, t)))
					except FileNotFoundError as err:
						erf = str(err).split(' ')[-1].strip('\'')
						if erf in dels:
							continue
						print(erf, dels)






if __name__ == '__main__':
	exit(1)
