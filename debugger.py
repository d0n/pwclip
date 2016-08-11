import sys
from os import getuid, makedirs
from os.path import \
    basename, expanduser

import logging

def logger(name):
	logdir = '/var/log/%s'%name
	if getuid() != 0:
		logdir = expanduser('~/log/%s'%name)
	logfile = '%s/%s.log'%(logdir, name)
	try: makedirs(logdir)
	except FileExistsError: pass
	logging.basicConfig(
        format='%(asctime)s %(name)s:%(levelname)s:%(funcName)s - %(message)s',
        level=logging.INFO, filename=logfile, datefmt='%FT%T%:z')
	return logging.getLogger(logfile)

