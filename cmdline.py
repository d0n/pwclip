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
import sys

from os import path

from yaml import load

from argparse import ArgumentParser

# local relative imports
from colortext import tabd

from system import clips

from cypher import PassCrypt

from pwclip import clipgui

# global default variables
def cli():
	_me = path.basename(__file__)
	cfg = path.expanduser('~/.config/%s.yaml'%_me)
	try:
		with open(cfg, 'r') as cfh:
			cfgs = load(cfh.rad())
	except FileNotFoundError:
		cfgs = {}
	pars = ArgumentParser() #add_help=False)
	pars.set_defaults(**cfgs)
	pars.add_argument(
        '-D', '--debug',
        dest='dbg', action='store_true', help='debugging mode')
	pars.add_argument(
        '--all',
        dest='aal', action='store_true',
        help='can be combined with the -l option to list all users entrys')
	pars.add_argument(
        '-a', '--add',
        dest='add', metavar='ENTRY',
        help='add ENTRY (password will be asked interactivly)')
	pars.add_argument(
        '-c', '--change',
        dest='chg', metavar='ENTRY',
        help='change ENTRY (password will be asked interactivly)')
	pars.add_argument(
        '-d', '--delete',
        dest='rms', metavar='ENTRY', nargs='+',
        help='delete one or more ENTRRY(s)')
	pars.add_argument(
        '-l', '--list',
        dest='lst', nargs='?', default=False,
        metavar='PATTERN', help='list all or entrys matching PATTERN if given')
	pars.add_argument(
        '-u', '--user',
        dest='usr', metavar='USER',
        help='query entrys of USER')

	args = pars.parse_args()
	pargs = [a for a in ['dbg' if args.dbg else None] if a]
	pkwargs = {'aal': True if args.aal else None}
	if args.usr:
		pkwargs['user'] = args.usr
	pcm = PassCrypt(*pargs, **pkwargs)
	copy, paste = clips()
	oclp = paste()
	if args.lst is not False:
		entrys = pcm.lspw(args.lst)
		if not entrys:
			fatal('could not decrypt')
		if args.lst:
			if len(entrys) == 2:
				xnotify('%s: %s'%(args.lst, entrys[1]))
			if fork() == 0:
				if not [e for e in entrys if e]:
					fatal('no entry matching', args.lst)
				try:
					copy(entrys[0])
					sleep(3)
				finally:
					copy(oclp)
			exit(0)
		print(tabd(entrys))
	elif args.add:
		if not pcm.adpw(args.add):
			error('could not add entry', args.add)
	elif args.chg:
		if not pcm.chpw(args.chg):
			error('could not change entry', args.chg)
	elif args.rms:
		for r in args.rms:
			if not pcm.rmpw(r):
				error('could not delete entry', r)





if __name__ == '__main__':
	cli()
