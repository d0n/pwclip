from re import search as _search, U as _U, A as _A
from os import urandom as _urandom

def random(limit=10, pattern='[\w -~]'):
	retstr = ''
	while len(retstr) < int(limit):
		try:
			out = _urandom(1).decode()
		except UnicodeDecodeError as err:
			continue
		if out and _search(r'%s'%(pattern), out):
			retstr = '%s%s'%(retstr, out.strip())
	return retstr

