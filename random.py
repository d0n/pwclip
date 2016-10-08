from sys import stdout as _stdout
from re import search as _search
from os import urandom as _urandom

def random(limit=10, regex='[\w -~]'):
	retstr = ''
	while True:
		try:
			out = _urandom(1).decode()
		except UnicodeDecodeError:
			continue
		if _search(regex, out).group(0):
			retstr = '%s%s'%(retstr, out.strip())
		if len(retstr) >= int(limit):
			break
	return retstr

