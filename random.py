from re import search as _search, U as __U__
from os import urandom as _urandom

def random(limit=10, pattern='[\w -~]'):
	rnds = ''
	while len(rnds) < int(limit):
		try:
			out = _urandom(1)
			out = out.decode()
		except UnicodeDecodeError as err:
			continue
		char = _search(r'%s'%(pattern), out, __U__)
		if char:
			rnds = '%s%s'%(rnds, out.strip())
	return rnds

