from os import stat
from time import time

def fileage(trgfile):
	trgtime = int(stat(trgfile).st_mtime)
	thetime = int(time())
	return int(thetime-trgtime)
