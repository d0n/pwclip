#!/usr/bin/env python3
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
"""pwclip main program"""
# global & stdlib imports
try:
	from os import fork
except ImportError:
	def fork(): """fork faker function""" ;return 0

from os import environ, path, remove, name as osname

from subprocess import call

from argparse import ArgumentParser

from argcomplete import autocomplete
#from argcomplete.completers import FilesCompleter, ChoicesCompleter

from time import sleep

from yaml import load

try:
	import readline
except ImportError:
	pass

# local relative imports
from colortext import bgre, tabd, error, fatal

from system import copy, paste, xgetpass, xmsgok, xyesno, xnotify, which

# first if on windows and gpg.exe cannot be found in PATH install gpg4win
if osname == 'nt' and not which('gpg.exe'):
	if not xyesno('gpg4win is mandatory! Install it?'):
		exit(1)
	import wget
	src = 'https://files.gpg4win.org/gpg4win-latest.exe'
	trg = path.join(environ['TEMP'], 'gpg4win.exe')
	wget.download(src, out=trg)
	try:
		call(trg)
	except TimeoutError:
		exit(1)
	finally:
		remove(trg)

from secrecy import PassCrypt, ykchalres

from pwclip.__pkginfo__ import version

def forkwaitclip(text, poclp, boclp, wait=3):
	"""clipboard forking, after time resetting function"""
	if fork() == 0:
		try:
			copy(text, mode='pb')
			sleep(int(wait))
		except (KeyboardInterrupt, RuntimeError):
			exit(1)
		finally:
			copy(poclp, mode='p')
			copy(boclp, mode='b')
	exit(0)

def confpars():
	"""pwclip command line opt/arg parsing function"""
	prol = 'pwclip - multi functional password manager to temporarily ' \
           'save passphrases  to your copy/paste buffers for easy and ' \
           'secure accessing your passwords'
	pars = ArgumentParser(description=prol) #add_help=False)
	pars.set_defaults(**cfgs)
	pars.add_argument(
        '--version',
        action='version', version='%(prog)s-v'+version)
	pars.add_argument(
        '-D', '--debug',
        dest='dbg', action='store_true', help='debugging mode')
	pars.add_argument(
        '-A', '--all',
        dest='aal', action='store_true',
        help='switch to all users entrys (instead of current user only)')
	pars.add_argument(
        '-o', '--stdout',
        dest='out', action='store_true',
        help='print received password to stdout (insecure & unrecommended)')
	pars.add_argument(
        '-s', '--show-passwords',
        dest='sho', action='store_true',
        help='switch to display passwords (replaced with * by default)')
	pars.add_argument(
        '-t',
        dest='time', default=3, metavar='seconds', type=int,
        help='time to wait before resetting clip (default is 3 max 3600)')

	rpars = pars.add_argument_group('remote arguments')
	rpars.add_argument(
        '-R',
        dest='rem', action='store_true',
        help='use remote backup given by --remote-host')
	rpars.add_argument(
        '--remote-host',
        dest='rehost', metavar='HOST',
        help='use HOST for connections')
	rpars.add_argument(
        '--remote-user',
        dest='reuser', metavar='USER',
        help='use USER for connections to HOST')

	gpars = pars.add_argument_group('gpg/ssl arguments')
	gpars.add_argument(
        '-r', '--recipients',
        dest='rcp', metavar='ID(s)',
        help='gpg-key ID(s) to use for ' \
             'encryption (string seperated by spaces)')
	gpars.add_argument(
        '-u', '--user',
        dest='usr', metavar='USER', default=cfgs['user'],
        help='query entrys only for USER ' \
             '(defaults to current user, overridden by -A)')
	gpars.add_argument(
        '-x', '--x509',
        dest='gpv', action='store_const', const='gpgsm',
        help='force ssl compatible gpgsm mode - usually is autodetected ' \
             '(use --cert --key for imports)')
	gpars.add_argument(
        '-C', '--cert',
        dest='sslcrt', metavar='SSL-Certificate',
        help='one-shot setting of SSL-Certificate')
	gpars.add_argument(
        '-K', '--key',
        dest='sslkey', metavar='SSL-Private-Key',
        help='one-shot setting of SSL-Private-Key')
	gpars.add_argument(
        '--ca', '--ca-cert',
        dest='sslca', metavar='SSL-CA-Certificate',
        help='one-shot setting of SSL-CA-Certificate')
	gpars.add_argument(
        '-P', '--passcrypt',
        dest='pcr', metavar='CRYPTFILE',
        default=path.expanduser('~/.passcrypt'),
        help='set location of CRYPTFILE to use for gpg features')
	gpars.add_argument(
        '-Y', '--yaml',
        dest='yml', metavar='YAMLFILE',
        default=path.expanduser('~/.pwd.yaml'),
        help='set location of one-time password YAMLFILE to read & delete')
	gpars.add_argument(
        '-S', '--slot',
        dest='ysl', default=None, type=int, choices=(1, 2),
        help='set one of the two slots on the yubi-key (only useful for -y)')

	ypars = pars.add_argument_group('yubikey arguments')
	ypars.add_argument(
        '-y', '--ykserial',
        nargs='?', dest='yks', metavar='SERIAL', default=False,
        help='switch to yubikey mode and optionally set SERIAL of yubikey')

	gpars = pars.add_argument_group('action arguments')
	gpars.add_argument(
        '-a', '--add',
        dest='add', metavar='ENTRY',
        help='add ENTRY (password will be asked interactivly)')
	gpars.add_argument(
        '-c', '--change',
        dest='chg', metavar='ENTRY',
        help='change ENTRY (password will be asked interactivly)')
	gpars.add_argument(
        '-d', '--delete',
        dest='rms', metavar='ENTRY', nargs='+',
        help='delete ENTRY(s) from the passcrypt list')
	gpars.add_argument(
        '-l', '--list',
        nargs='?', dest='lst', metavar='PATTERN', default=False,
        help='search entry matching PATTERN if given otherwise list all')

	autocomplete(pars)
	args = pars.parse_args()
	return pars, args

def gui(typ='pw'):
	"""gui wrapper function to not run unnecessary code"""
	poclp, boclp = paste('pb')
	pars, cfgs = confpars()
	print(cfgs)
	if args.yks is False and args.lst is False and \
	      args.add is None and args.chg is None and \
	     args.rms is None and (args.sslcrt is None and args.sslkey is None):
		pars.print_help()
	exit()
	if typ == 'yk':
		__in = xgetpass()
		__res = ykchalres(__in, cfgs['ykslot'], cfgs['ykser'])
		if not __res:
			xmsgok('no entry found for %s or decryption failed'%__in)
			exit(1)
		forkwaitclip(__res, poclp, boclp, cfgs['time'])
	pcm = PassCrypt(**cfgs)
	__in = xgetpass()
	if not __in: exit(1)
	__ent = pcm.lspw(__in)
	if __ent and __in:
		if __in not in __ent.keys() or not __ent[__in]:
			xmsgok('no entry found for %s'%__in)
			exit(1)
		__pc = __ent[__in]
		if __pc:
			if len(__pc) == 2:
				xnotify('%s: %s'%(__in, __pc[1]), cfgs['time'])
			poclp, boclp = paste('pb')
			forkwaitclip(__pc[0], poclp, boclp, cfgs['time'])


if __name__ == '__main__':
	exit(1)
