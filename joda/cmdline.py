# -*- coding: utf-8 -*-
#
# This file is free software by Leon Pelzer <leon.pelzer@1und1.de>
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
# (std)lib imports
from os import \
    getcwd as _getcwd, \
    environ as _environ

from os.path import \
    expanduser as _expanduser, \
    isfile as _isfile, \
    basename as _basename, \
    dirname as _dirname

from re import \
    search as _search

from socket import \
    gethostbyname as _host, \
    gaierror as _dnserror

from sys import \
    argv as _argv, \
    stdout as _stdout, \
    stderr as _stderr
__echo = _stdout.write
__puke = _stderr.write

from os.path import \
    basename as _basename

from yaml import \
    load as _load

from argparse import \
    ArgumentParser as _ArgumentParser, \
    SUPPRESS as _SUPPRESS

# local relative import
from salt.modules import \
    jboss7 as _jboss7, \
    jboss7_cli as jboss7_cli

try:
	from argparse import \
        ArgumentParser as _ArgParser

	from argcomplete import \
        autocomplete as _autocomplete

	from argcomplete.completers import \
        FilesCompleter as _FilesCompleter, \
        ChoicesCompleter as _ChoicesCompleter
except:
    __puke('could not import bash-cli-argument-completer...\n')

def __isip(pattern):
	# return True if "pattern" is RFC conform IP otherwise False
	iplike = '^(?!0+\.0+\.0+\.0+|255\.255\.255\.255)' \
        '(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)' \
        '\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
	if _search(iplike, pattern):
		return True
	return False

def __loadconfs(config):
	cfgs = {}
	if _isfile(config):
		with open(config, 'r') as cfg:
			cfgs = _load(cfg)
		cfgs.update(
            dict(('dbg', v) for (
                k, v) in cfgs.items() if k == 'debug'))
		cfgs.update(
            dict(('vrb', v) for (
                k, v) in cfgs.items() if k == 'verbose'))
		cfgs.update(
            dict((k, _expanduser(v)) for (
                k, v) in cfgs.items() if str(v).startswith('~')))
		cfgs.update(
            dict((k, '%s/%s'%(_dirname(__file__), v[2:])) for (
                k, v) in cfgs.items() if str(v).startswith('./')))
	return cfgs

def _slotport(slotnum):
	port = 9999
	if slotnum:
		port = port + (slotnum * 100)
	return port

def argrevert(val):
	return 'store_false' if val else 'store_true'

def trbool(val):
	return 'enabled' if val else 'disabled'

def _jbstat(fqdn, confset):
	__echo('status of %s:\n'%fqdn)
	prind(_jboss7.status(confset), pfix='  ', end=2)

def _jbdslist(fqdn, confset):
	__echo('datasources of %s:\n'%fqdn)
	prind(_jboss7.list_datasources(confset), pfix='  ')

def _jbdpls(fqdn, confset):
	__echo('deployments of %s:\n  %s\n'%(
        fqdn,
        '\n  '.join(d for d in _jboss7.list_deployments(confset).split('\n'))))


def _jbdsread(fqdn, name, confset):
	__echo('datasource %s of %s:\n'%(name, fqdn))
	dsprops = _jboss7.read_datasource(confset, name)
	prind(dsprops['result'], pfix='  ')

def prind(dic, pfix='', end=1):
	def __dictprinter(dic):
		lim = max(len(k) for k in dic.keys())
		__echo('\n'.join('%s%s%s= %s'%(
            pfix, key, ' '*int(lim-len(key)+2), val) for (key, val) in dic.items()))
	if isinstance(dic, dict):
		__dictprinter(dic)
	elif isinstance(dic, list):
		for d in dic:
			if isinstance(d, dict):
				__dictprinter(d)
			else:
				__echo('%s%s\n'%(pfix, d))
	else:
		__echo('%s%s'%(pfix, dic))
	if end > 0:
		__echo('\n'*end)

def cli():
	"""joda command line function"""
	__me__ = _argv[0].split('/')[-1].split('.')[0]
	__version__ = '0.0.1'
	__cfgfile = _expanduser('~/.config/%s.conf'%__me__)
	__dsc = '%s <by leon.pelzer@1und1.de> Junk Operator-Dummy Application ' \
        '- convenience wrapper around the salt-stack implemented jboss-cli ' \
        'wrapper providing remote jboss admnistration functionality'%__me__
	__epi = 'all settings might also be set by the configuration file ' \
        'args.fqdns might be provided by using the --slot argument in ' \
        'combination with a bare fqdn or ip or by providing them ' \
        'colon seperated (fqdn/ip:port)'
	__cfgs = {'dbg': False, 'vrb': False}
	__cfgs.update(__loadconfs(__cfgfile))

	pars = _ArgumentParser(description=__dsc, epilog=__epi)
	addgroup = pars.add_argument_group
	pars.set_defaults(**__cfgs)
	pars.add_argument(
        '--version',
        action='version', version='%(prog)s v'+__version__)
	bhas = addgroup('behaviour')
	bhas.add_argument(
        '--debug',
        dest='dbg',
        action=argrevert(__cfgs['dbg']),
        help='switch on/off debugging output (is %s)'%(trbool(__cfgs['dbg'])))
	bhas.add_argument(
        '--verbose',
        dest='vrb', action=argrevert(__cfgs['vrb']),
        help='switch on/off verbose output (is %s)'%(trbool(__cfgs['vrb'])))
	cfgs = addgroup('configuration')
	cfgs.add_argument(
        '--cli',
        dest='jbosscli',
        help='path to jboss-cli')
	cfgs.add_argument(
        '--java-home',
        dest='javahome',
        help='path to java (containing it\'s bin/ folder)')
	cfgs.add_argument(
        '--cli-user',
        dest='cliuser',
        help='the username used for cli login')
	cfgs.add_argument(
        '--cli-pw',
        dest='clipass',
        help='the password used for cli login')
	cfgs.add_argument(
        '-s', '--slot',
        dest='slotnum', type=int,
        help='the args.fqdn jboss slot (used for port guessing)')
	qrys = addgroup('querys')
	qrys.add_argument(
        '-l', '--list',
        dest='dls', action='store_true',
        help='list args.fqdns current deployments')
	qrys.add_argument(
        '--status',
        dest='sts', action='store_true',
        help='list args.fqdns current deployments')
	qrys.add_argument(
        '--dsinfo',
        dest='dinfo', metavar='NAME',
        help='show datasource information')
	qrys.add_argument(
        '--bdinfo',
        dest='binfo', metavar='NAME',
        help='show binding information')
	acts = addgroup('actions')
	acts.add_argument(
        '-r', '--restart',
        dest='rbt', action='store_true',
        help='restart args.fqdn runtime instance')
	acts.add_argument(
        '--start',
        dest='sta', action='store_true',
        help='start args.fqdn runtime instance')
	acts.add_argument(
        '--reload',
        dest='rld', action='store_true',
        help='reload configuration on args.fqdn')
	acts.add_argument(
        '--stop',
        dest='stp', action='store_true',
        help='shutdown args.fqdn runtime instance')

	bnds = addgroup('binding')
	bnds.add_argument(
        '--create-binding',
        dest='binding', help='create a binding on args.fqdn instance')
	bnds.add_argument(
        '--delete-binding',
        dest='binding', help='delete a binding on args.fqdn instance')
	bnds.add_argument(
        '--update-binding',
        dest='binding', help='update a binding on args.fqdn instance')

	"""
	dpls = addgroup('deployment')
	dpls.add_argument(
        '-d', '--deploy',
        dest='dodeploy', metavar='ARTIFACT',
        help='deploy an artifact on args.fqdn')
	dpls.add_argument(
        '-u', '--undeploy',
        dest='undeploy', metavar='ARTIFACT',
        help='undeploy an artifact on args.fqdn')
	"""

	srcs = addgroup('datasource')
	srcs.add_argument(
        '-d', '--dslist',
        action='store_true',
        help='list all datasources for target')
	srcs.add_argument(
        '--dscreate',
        metavar=('DSNAME', 'DSPROPERTIES'), nargs=2,
        help='create DATASOURCE on args.fqdn')
	srcs.add_argument(
        '--dsprops',
        metavar='PROPERTIES',
        help='provide additional datasource properties')
	srcs.add_argument(
        '--dsdelete',
        metavar='DATASOURCE',
        help='delete datasource on args.fqdn')
	srcs.add_argument(
        '--dsupdate',
        metavar=('DSNAME', 'DSPROPERTIES'), nargs=2,
        help='update an existing datasource on args.fqdn')
	srcs.add_argument(
        '--dsread',
        dest='dsread', metavar='DATASOURCE',
        help='read data of existing datasource on args.fqdn')

	trgs = addgroup('args.fqdn')
	trgs.add_argument(
        'fqdn',
        metavar='fqdn[:port]',
        help='fqdn or numeric (ip:port) args.fqdn(s)')

	try:
		_autocomplete(pars)
	except NameError:
		# while this is just a continuation failure from the above
		# missing import we just suppress this
		pass
		
	args = pars.parse_args()

	jbosscli = args.jbosscli if args.jbosscli else \
        '%s/jbcli/bin/jboss-cli.sh'%(_dirname(__file__))
	javahome = args.javahome if args.javahome else \
        '%s/orjdk'%(_dirname(__file__))
	_environ['PATH'] = '%s/bin:%s'%(javahome, _environ['PATH'])
	_environ['JAVA_HOME'] = javahome

	confset = {
        '__dbg__': True if args.dbg else False,
        'cli_path': jbosscli,
        'cli_user': args.cliuser,
        'cli_password': args.clipass}

	if args.slotnum:
		port = _slotport(args.slotnum)

	fqdn = args.fqdn

	if ':' in fqdn:
		fqdn, port = fqdn.split(':')
	else:
		if not args.slotnum:
			pars.print_usage()
			prind('\033[31mincomplete configuration - ' \
				'use -s/--slot to provide the port\nor append it ' \
				'to the args.fqdn seperated by a colon\033[0m')
			exit(1)
	if not __isip(fqdn):
		try:
			fqdn = _host(fqdn)
		except _dnserror:
			prind('\033[31minvalid args.fqdn \033[33m%s\033[0m'%fqdn)
	fqdn = '%s:%s'%(fqdn, port)
	confset['controller'] = fqdn


	if args.dbg:
		prind(dict(args.__dict__.items()))
		prind({'confset': confset}, pfix='  ', end=2)
	if not args.fqdn:
		pars.print_help()
		prind('\033[01;31mFATAL: need args.fqdn\033[0m')
		exit(1)


	if args.sts:
		_jbstat(args.fqdn, confset)
	elif args.dls:
		_jbdpls(args.fqdn, confset)

	elif args.dslist:
		_jbdslist(args.fqdn, confset)

	elif args.dscreate:
		dsprops = {}
		for keyval in args.dscreate[1].strip('{}').split(','):
			dsprops[keyval.split(':')[0].strip()] = \
                ':'.join(k for k in keyval.split(':')[1:]).strip()
		prind(_jboss7.create_datasource(confset, args.dscreate[0], dsprops))
	elif args.dsupdate:
		prind(_jboss7.update_datasource(
            confset, args.dsupdate[0], args.dsupdate[1]), pfix='  ')
	elif args.dsread:
		_jbdsread(args.fqdn, args.dsread, confset)
	elif args.dsdelete:
		prind(_jboss7.remove_datasource(confset, args.dsdelete), pfix='  ')
	else:
		_jbstat(args.fqdn, confset)

