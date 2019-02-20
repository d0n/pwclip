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

from os import environ, path, remove, getpid, name as osname

from subprocess import DEVNULL, Popen, call

from argparse import ArgumentParser

from argcomplete import autocomplete
from argcomplete.completers import FilesCompleter, ChoicesCompleter

from socket import gethostname as hostname

from time import sleep

from yaml import load

from getpass import getpass

# local relative imports
from colortext import bgre, bred, tabd, error, fatal

from system import copy, paste, xgetpass, xmsgok, xyesno, xnotify, which

from secrecy import PassCrypt, ykchalres, yubikeys

from pwclip.__pkginfo__ import version

def forkwaitclip(text, poclp, boclp, wait=3, out=None):
	"""clipboard forking, after time resetting function"""
	fno = fork()
	if out == 'gui' and fno == 0:
		Popen(str(
			'xvkbd -no-keypad -delay 20 -text %s'%text
		).split(' '), stdout=DEVNULL, stderr=DEVNULL).communicate()
	elif out == 'cli' and fno == 0:
		print(text, end='')
	print(text)
	if fno == 0:
		copy(text, mode='pb')
		try:
			sleep(int(wait))
		except KeyboardInterrupt:
			exit(1)
		finally:
			copy(poclp, mode='p')
			copy(boclp, mode='b')
		exit(0)
	exit(0)

def __passreplace(pwlist):
	"""returnes a string of asterisk's as long as the password is"""
	__pwcom = ['*'*len(str(pwlist[0]))]
	if len(pwlist) > 1:
		__pwcom.append(pwlist[1])
	return __pwcom

def __dictreplace(pwdict):
	"""password => asterisk replacement function"""
	__pwdict = {}
	for (usr, ent) in pwdict.items():
		if isinstance(ent, dict):
			__pwdict[usr] = {}
			for (u, e) in ent.items():
				__pwdict[usr][u] = __passreplace(e)
		elif ent:
			__pwdict[usr] = __passreplace(ent)
	return __pwdict

def _printpws_(pwdict, insecure=False):
	"""password printer with in/secure option"""
	if not insecure:
		pwdict = __dictreplace(pwdict)
	print(tabd(pwdict))
	exit(0)

def confpars(mode):
	"""pwclip command line opt/arg parsing function"""
	_me = path.basename(path.dirname(__file__))
	cfg = path.expanduser('~/.config/%s.yaml'%_me)
	try:
		with open(cfg, 'r') as cfh:
			cfgs = load(cfh.read())
	except FileNotFoundError:
		cfgs = {}
	try:
		cfgs['time'] = environ['PWCLIPTIME']
	except KeyError:
		cfgs['time'] = 3 if 'time' not in cfgs.keys() else cfgs['time']
	try:
		cfgs['ykslot'] = environ['YKSLOT']
	except KeyError:
		cfgs['ykslot'] = None
	try:
		cfgs['ykser'] = environ['YKSERIAL']
	except KeyError:
		cfgs['ykser'] = None
	try:
		cfgs['binary']
	except KeyError:
		cfgs['binary'] = 'gpg2'
		if osname == 'nt':
			cfgs['binary'] = 'gpg'
	try:
		cfgs['user'] = environ['USER']
	except KeyError:
		cfgs['user'] = environ['USERNAME']
	if 'crypt' not in cfgs.keys():
		cfgs['crypt'] = path.expanduser('~/.passcrypt')
	elif 'crypt' in cfgs.keys() and cfgs['crypt'].startswith('~'):
		cfgs['crypt'] = path.expanduser(cfgs['crypt'])
	if 'plain' not in cfgs.keys():
		cfgs['plain'] = path.expanduser('~/.pwd.yaml')
	elif 'plain' in cfgs.keys() and cfgs['plain'].startswith('~'):
		cfgs['plain'] = path.expanduser(cfgs['plain'])
	desc = 'pwclip - Multi functional password manager to temporarily ' \
           'save passphrases to your copy/paste buffers for easy and ' \
           'secure accessing your passwords. The following ' \
           'arguments mights also be set by the config ' \
           '~/.config/%s.yaml file.'%_me
	epic = 'the yubikey mode is compatible with the ' \
           'challenge-response feature of yubikeys only for now.'
	pars = ArgumentParser(description=desc, epilog=epic)
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
        help='switch to all users entrys ("%s" only is default)'%cfgs['user'])
	pars.add_argument(
        '-o', '--stdout',
        dest='out', action='store_const', const=mode,
        help='print password to stdout (insecure and unrecommended)')
	pars.add_argument(
        '-s', '--show-passwords',
        dest='sho', action='store_true',
        help='show passwords when listing (replaced by "*" is default)')
	pars.add_argument(
        '-t',
        dest='time', default=3, metavar='seconds', type=int,
        help='time to wait before resetting clip (%s is default)'%cfgs['time'])
	pars.add_argument(
        '-P', '--passcrypt',
        dest='pcr', metavar='CRYPTFILE',
        default=path.expanduser('~/.passcrypt'),
        help='set location of CRYPTFILE to use as ' \
             'password store (~/.passcrypt is default)')
	pars.add_argument(
        '-u', '--user',
        dest='usr', metavar='USER', default=cfgs['user'],
        help='query entrys only for USER (-A overrides, ' \
             '"%s" is default)'%cfgs['user'])
	pars.add_argument(
        '-Y', '--yaml',
        dest='yml', metavar='YAMLFILE',
        default=path.expanduser('~/.pwd.yaml'),
        help='set location of YAMLFILE to read whole ' \
             'sets of passwords from a yaml file (~/.pwd.yaml is default)')
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
        help='use USER for connections to HOST ("%s" is default)'%cfgs['user'])
	gpars = pars.add_argument_group('gpg/ssl arguments')
	gpars.add_argument(
        '-r', '--recipients',
        dest='rcp', metavar='"ID ..."',
        help='one ore more gpg-key ID(s) to use for ' \
             'encryption (strings seperated by spaces within "")')
	pars.add_argument(
        '-p', '--password',
        dest='pwd', default=None,
        help='enter password for add/change action' \
             '(insecure & not recommended)')
	pars.add_argument(
        '--comment',
        dest='com', default=None,
        help='enter comment for add/change action')
	gpars.add_argument(
        '-x', '--x509',
        dest='gpv', action='store_const', const='gpgsm',
        help='force ssl compatible gpgsm mode - usually is autodetected ' \
             '(use --cert & --key for imports)')
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

	
	ypars = pars.add_argument_group('yubikey arguments')
	ypars.add_argument(
        '-S', '--slot',
        dest='ysl', default=None, type=int, choices=(1, 2),
        help='set one of the two yubikey slots (only useful with -y)'
			).completer = ChoicesCompleter((1, 2))
	ypars.add_argument(
        '-y', '--ykserial',
        nargs='?', dest='yks', metavar='SERIAL', default=False,
        help='switch to yubikey mode and optionally set ' \
		     'SERIAL of yubikey (autoselect serial and slot is default)')
				
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
        help='pwclip an entry matching PATTERN if given ' \
             '- otherwise list all entrys')
	autocomplete(pars)
	args = pars.parse_args()
	pargs = [a for a in [
        'aal' if args.aal else None,
        'dbg' if args.dbg else None,
        'gsm' if args.gpv else None,
		'gui' if mode else None,
        'rem' if args.sho else None,
        'sho' if args.sho else None] if a]
	__bin = 'gpg2'
	if args.gpv:
		__bin = args.gpv
	if osname == 'nt':
		__bin = 'gpgsm.exe' if args.gpv else 'gpg.exe'
	pkwargs = {}
	pkwargs['binary'] = __bin
	pkwargs['sslcrt'] = args.sslcrt
	pkwargs['sslkey'] = args.sslkey
	if args.pcr:
		pkwargs['crypt'] = args.pcr
	if args.rcp:
		pkwargs['recvs'] = list(args.rcp.split(' '))
	if args.usr:
		pkwargs['user'] = args.usr
	if args.time:
		pkwargs['time'] = args.time
	if args.yml:
		pkwargs['plain'] = args.yml
	if hasattr(args, 'remote'):
		pkwargs['remote'] = args.remote
	if hasattr(args, 'reuser'):
		pkwargs['reuser'] = args.reuser
	if args.dbg:
		print(bgre(pars))
		print(bgre(tabd(args.__dict__, 2)))
		print(bgre(pkwargs))
	if mode == 'gui':
		return args, pargs, pkwargs
	if (
          args.yks is False and args.lst is False and \
          args.add is None and args.chg is None and \
          args.rms is None and (args.sslcrt is None and args.sslkey is None)):
		pars.print_help()
		exit(0)
	return args, pargs, pkwargs

def cli():
	args, pargs, pkwargs = confpars('cli')
	if not path.isfile(args.yml) and \
          not path.isfile(args.pcr) and args.yks is False:
		with open(args.yml, 'w+') as yfh:
			yfh.write("""---\n%s:  {}"""%args.usr)
	poclp, boclp = paste('pb')
	if args.yks or args.yks is None:
		if 'YKSERIAL' in environ.keys():
			ykser = environ['YKSERIAL']
		ykser = args.yks if args.yks else None
		if ykser and len(ykser) >= 6:
			ykser = ''.join(str(ykser)[-6:])
		res = ykchalres(getpass(), args.ysl, ykser)
		if not res:
			fatal('could not get valid response on slot ', args.ysl)
		forkwaitclip(res, poclp, boclp, args.time, args.out)
		exit(0)
	__ents = {}
	err = None
	if args.add:
		__ents = PassCrypt(*pargs, **pkwargs).adpw(
            args.add, args.pwd, args.com)
		if not args.aal:
			__ents = __ents[args.user]
		if not __ents or args.add not in __ents.keys():
			err = ('could not add entry', args.add)
	elif args.chg:
		if args.pwd:
			pkwargs['password'] = args.pwd
		__ents = PassCrypt(*pargs, **pkwargs).chpw(
            args.chg, args.pwd, args.com)
		if not args.aal:
			__ents[args.user]
		if not __ents:
			if [h for (u, es) in __ents.items() if args.chg in en.keys()]:
				exit(0)
			err = ('could not change entry', args.chg)
	elif args.rms:
		ers = []
		for r in args.rms:
			__ents = PassCrypt(*pargs, **pkwargs).rmpw(r)
			if not args.aal:
				__ents[args.user]
			if r in __ents.keys():
				ers.append(r)
		ewrd = 'entry'
		if len(ers) >= 1:
			ewrd = 'entrys'
		err = ('deleting the following %s failed:', bred(', ').join(
               ers)) if ers else None
	elif args.lst is not False and args.lst is not None:
		__ents = PassCrypt(*pargs, **pkwargs).lspw(args.lst)
		if __ents and args.lst not in __ents.keys():
			err = (
                'could not find entry', args.lst,
                'for', args.user, 'in', pkwargs['crypt'])
		elif args.lst and __ents:
			__pc = __ents[args.lst]
			if __pc:
				if len(__pc) == 2 and osname != 'nt':
					xnotify('%s: %s'%(
                        args.lst, ' '.join(__pc[1:])), args.time)
				forkwaitclip(__pc[0], poclp, boclp, args.time, args.out)
				exit(0)
	elif args.lst is None:
		__ents = PassCrypt(*pargs, **pkwargs).lspw()
	if err:
		fatal(*err)
	_printpws_(__ents, args.sho)

def gui(typ='pw'):
	"""gui wrapper function to not run unnecessary code"""
	poclp, boclp = paste('pb')
	args, pargs, pkwargs = confpars('gui')
	if args.yks or args.yks is None or typ == 'yk':
		res = ykchalres(xgetpass(), args.ykslot, args.ykser)
		if not res:
			if xyesno('entry %s does not ' \
                  'exist or decryption failed\ntry again?'%__in):
				exit(1)
		eno = forkwaitclip(res, poclp, boclp, args.time, args.out)
		exit(eno)
	pcm = PassCrypt(*pargs, **pkwargs)
	while True:
		fork = 0
		if args.add:
			if not PassCrypt(
                  *pargs, **pkwargs).adpw(args.add, args.pwd, args.com):
				xmsgok('could not add entry %s'%args.add)
				exit(1)
			exit(0)
		elif args.chg:
			if args.pwd:
				pkwargs['password'] = args.pwd
			if not PassCrypt(
                  *pargs, **pkwargs).chpw(args.chg, args.pwd, args.com):
				xmsgok('could not change entry %s'%args.chg)
				exit(1)
			exit(0)
		elif args.rms:
			for r in args.rms:
				__ents = PassCrypt(*pargs, **pkwargs).rmpw(r)
				if not __ents:
					xmsgok('could not delete entry %s'%args.rms)
					exit(1)
			exit(0)
		__in = args.lst if args.lst else xgetpass()
		if not __in:
			if xyesno('no input received, try again?'):
				continue
			exit(1)
		__ent = pcm.lspw(__in)
		if not __ent or __ent and __in not in __ent.keys() or not __ent[__in]:
			if xyesno('no entry found for %s matching %s, try again?'%(
                  args.usr, __in)):
				continue
			exit(1)
		if __ent:
			__pc = __ent[__in]
			if __pc:
				if len(__pc) == 2:
					xnotify('%s: %s'%(__in, ' '.join(__pc[1:])), args.time)
				forkwaitclip(__pc[0], poclp, boclp, args.time, args.out)
				exit(0)
