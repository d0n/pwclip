#!/usr/bin/env /usr/bin/python3
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
"""module disclaimer"""

# global & stdlib imports
#import re
import os
import sys

# local relative imports
from lib.misc import which
from lib.colortext import blu, grn, yel, abort, error
from lib.executor import Command

# global default variables
__version__ = '0.0'

class SubVersion(Command):
	_sh_ = True
	_svnbin = which('svn')
	@property               # svnbin <str>
	def svnbin(self):
		return self._svnbin

	def svndiffs(self, path, pattern=None, verbose=None):
		def __diffout(diff):
			diffout = ''
			for line in diff.split('\\n'):
				if '\\t' in line:
					for tabt in line.split('\\t'):
						diffout = '%s%s\t'%(diffout, tabt)
					diffout = '%s\n'%diffout
				else:
					diffout = '%s\n'%(diffout, line)
			return diffout
		def __revs(svnfile):
			revs = []
			output = self.stdx(
			    '%s log %s -q --stop-on-copy'%(self.svnbin, svnfile))
			for line in output.split('\n'):
				if line.startswith('r'):
					revs.append(str(line.split(' ')[0])[1:])
			return revs
		for rev in __revs(path):
			lastrev = ((int(rev)-1))
			if verbose:
				print(
					blu('comparing revision'),
					yel(lastrev), blu('and'), yel(rev))
			diff = self.stdx(
				'%s diff --old=%s@%s --new=%s@%s'%(
					self.svnbin, path, lastrev, path, rev
				))
			if pattern and not pattern in diff:
				continue
			yield diff
			"""
			if diff:
				dout = ''
				if not verbose:
					dout = '%s%s:\n'%(dout, rev)
				if pattern:
					dout = '%s\n%s'%()
					print(pattern)
					if pattern in diff:
						__diffout(diff)
				else:
					__diffout(diff)
			"""

	def svnstatus(self):
		status = self.stdx('%s status'%(self.svnbin))
		if status:
			return status.split('\n')

	def svndel(self):
		status = self.svnstatus()
		if status and [l for l in status if l.startswith('!')]:
			for line in status:
				if line.startswith('!'):
					delfile = line.split()[1]
					self.call('%s rm %s'%(self.svnbin, delfile))
			return True

	def svnadd(self):
		status = self.svnstatus()
		if status and [l for l in status if l.startswith('?')]:
			for line in status:
				if line.startswith('?'):
					addfile = line.split()[1]
					self.call('%s add %s'%(self.svnbin, addfile))
			return True

	def svncommit(self, message, autoadd=True):
		print(blu('cleaning up deleted files'))
		self.svndel()
		print(blu('updating svn repo'))
		self.call('%s up'%(self.svnbin))
		print()
		status = self.svnstatus()
		if status:
			if self.svnadd():
				status = self.svnstatus()
			if self.svndel():
				status = self.svnstatus()
			print('\n'.join(l for l in status))
			print(
			    blu('committing the above changes with message'),
			    '%s%s'%(yel(message), blu('...')))
			input(grn('press any key to continue\n'))
			commit = '%s commit -m "%s"' %(self.svnbin, message)
			return int(self.call(commit))
		print(blu('nothing to commit'))







if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
