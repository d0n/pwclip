from os import walk

from os.path import basename, exists, isdir, expanduser

from colortext import blu, yel, bgre
from system.path import absrelpath

def baserepos(bases, ignores, dbg=False):
	if dbg:
		print(bgre(_baserepos))
	gits = []
	svns = []
	for base in sorted(bases):
		base = absrelpath(base)
		if not isdir(base):
			continue
		elif exists('%s/.git'%base) and not \
              base in gits and not base in ignores:
			gits.append(base)
		elif '.svn' in base and not base in svns:
			svns.append(base)
		else:
			for (d, subs, files) in walk(base):
				if [i for i in ignores if i in d]:
					continue
				for s in subs:
					if [i for i in ignores if '%s/%s'%(d, s) in i]:
						continue
					if isdir('%s/%s/.git'%(d, s)):
						gits.append('%s/%s'%(d, s))
	rpotypes = {'git': gits, 'svn': svns}
	for typ in ('git', 'svn'):
		if rpotypes[typ] == []:
			del rpotypes[typ]
	return rpotypes
