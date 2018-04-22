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
"""pwclip cli program"""
from pwclip.pwclip import confpars, forkwaitclip
from secrecy import PassCrypt, ykchalres

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

def cli():
	args = confpars()
	__pargs = [a for a in [
        'aal' if args.aal else None,
        'dbg' if args.dbg else None,
        'gsm' if args.gpv else None,
        'rem' if args.sho else None,
        'sho' if args.sho else None] if a]
	__bin = 'gpg2'
	if args.gpv:
		__bin = args.gpv
	if osname == 'nt':
		__bin = 'gpgsm.exe' if args.gpv else 'gpg.exe'
	__pkwargs = {}
	__pkwargs['binary'] = __bin
	__pkwargs['sslcrt'] = args.sslcrt
	__pkwargs['sslkey'] = args.sslkey
	if args.pcr:
		__pkwargs['crypt'] = args.pcr
	if args.rcp:
		__pkwargs['recvs'] = list(args.rcp.split(' '))
	if args.usr:
		__pkwargs['user'] = args.usr
	if args.time:
		__pkwargs['time'] = args.time
	if args.yml:
		__pkwargs['plain'] = args.yml
	if hasattr(args, 'remote'):
		__pkwargs['remote'] = args.remote
	if hasattr(args, 'reuser'):
		__pkwargs['reuser'] = args.reuser
	if args.dbg:
		print(bgre(pars))
		print(bgre(tabd(args.__dict__, 2)))
		print(bgre(__pkwargs))
	if not path.isfile(args.yml) and \
          not path.isfile(args.pcr) and args.yks is False:
		with open(args.yml, 'w+') as yfh:
			yfh.write("""---\n%s:  {}"""%args.usr)
	poclp, boclp = paste('pb')
	if args.yks or args.yks is None:
		if 'YKSERIAL' in environ.keys():
			__ykser = environ['YKSERIAL']
		__ykser = args.yks if args.yks and len(args.yks) >= 6 else None
		__in = xgetpass()
		__res = ykchalres(__in, args.ysl, __ykser)
		if not __res:
			fatal('could not get valid response on slot ', args.ysl)
		forkwaitclip(__res, poclp, boclp, args.time)
	else:
		pcm = PassCrypt(*__pargs, **__pkwargs)
		__ent = None
		if args.add:
			if not pcm.adpw(args.add):
				fatal('could not add entry ', args.add)
			_printpws_(pcm.lspw(args.add), args.sho)
		elif args.chg:
			if not pcm.chpw(args.chg):
				fatal('could not change entry ', args.chg)
			_printpws_(pcm.lspw(args.chg), args.sho)
		elif args.rms:
			for r in args.rms:
				if not pcm.rmpw(r):
					error('could not delete entry ', r)
			_printpws_(pcm.lspw(), args.sho)
		elif args.lst is not False:
			__ent = pcm.lspw(args.lst)
			if not __ent:
				fatal('could not decrypt')
			elif __ent and args.lst and not args.lst in __ent.keys():
				fatal(
                    'could not find entry for ',
                    args.lst, ' in ', __pkwargs['crypt'])
			elif args.lst and __ent:
				__pc = __ent[args.lst]
				if __pc and args.out:
					print(__pc[0], end='')
					if len(__pc) == 2:
						xnotify('%s: %s'%(
                            args.lst, ' '.join(__pc[1:])), args.time)
					exit(0)
				elif __pc:
					if len(__pc) == 2:
						xnotify('%s: %s'%(
                            args.lst, __pc[1]), wait=args.time)
					copy(__pc[0], 'pb')
					forkwaitclip(__pc[0], poclp, boclp, args.time)
		else:
			__in = xgetpass()
			if not __in: exit(1)
			__ent = pcm.lspw(__in)
			if __ent and __in:
				if __in not in __ent.keys() or not __ent[__in]:
					fatal(
                        'could not find entry for ',
                        __in, ' in ', __pkwargs['crypt'])
				__pc = __ent[__in]
				if __pc:
					if len(__pc) == 2:
						xnotify('%s: %s'%(__in, __pc[1:]), args.time)
					copy(__pc[0], 'pb')
					forkwaitclip(__pc[0], poclp, boclp, args.time)
		if __ent:
			_printpws_(__ent, args.sho)
	try:
		readline.clear_history()
	except UnboundLocalError:
		pass



if __name__ == '__main__':
	exit(1)
