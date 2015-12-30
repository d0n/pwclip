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
"""gpg.py main program"""

from . import _gpgme
"""
    >>> Context
    >>> GenkeyResult
    >>> GpgmeError
    >>> ImportResult
    >>> Key
    >>> KeyIter
    >>> KeySig
    >>> NewSignature
    >>> Signature
    >>> Subkey
    >>> UserId
    >>> __doc__
    >>> __file__
    >>> __loader__
    >>> __name__
    >>> __package__
    >>> __spec__
    >>> gpgme_version
    >>> make_constants
"""

#_gpgme.make_constants(globals())

def libout():
	print(_gpgme)
	print('\n'.join(c for c in dir(_gpgme) if c.startswith('__') and c.endswith('__')), '\n')
	for mod in sorted(dir(_gpgme)):
		if mod.startswith('__') and mod.endswith('__'):
			continue
		print()
		print(mod)
		if mod == 'Context':
			print('\n'.join(c for c in dir(_gpgme.Context) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.Context):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'GenkeyResult':
			print('\n'.join(c for c in dir(_gpgme.GenkeyResult) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.GenkeyResult):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'GpgmeError':
			print('\n'.join(c for c in dir(_gpgme.GpgmeError) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.GpgmeError):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'ImportResult':
			print('\n'.join(c for c in dir(_gpgme.ImportResult) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.ImportResult):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'Key':
			print('\n'.join(c for c in dir(_gpgme.Key) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.Key):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'KeyIter':
			print('\n'.join(c for c in dir(_gpgme.KeyIter) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.KeyIter):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'KeySig':
			print('\n'.join(c for c in dir(_gpgme.KeySig) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.KeySig):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'NewSignature':
			print('\n'.join(c for c in dir(_gpgme.NewSignature) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.NewSignature):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'Signature':
			print('\n'.join(c for c in dir(_gpgme.Signature) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.Signature):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'Subkey':
			print('\n'.join(c for c in dir(_gpgme.Subkey) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.Subkey):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'UserId':
			print('\n'.join(c for c in dir(_gpgme.UserId) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.UserId):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'gpgme_version':
			print('\n'.join(c for c in dir(_gpgme.gpgme_version) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.gpgme_version):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
		elif mod == 'make_constants':
			print('\n'.join(c for c in dir(_gpgme.make_constants) if c.startswith('__') and c.endswith('__')))
			for fun in dir(_gpgme.make_constants):
				if fun.startswith('__') and fun.endswith('__'):
					continue
				print('  >>>', fun)
