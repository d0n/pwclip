import sys
from os.path import \
    basename, expanduser
from yaml import \
    load
import logging

def logger(lvl='INFO'):
	"""
	CRITICAL: 50
	ERROR:    40
	WARNING:  30
	INFO:     20
	DEBUG:    10
	NOTSET:   0
	"""
	prog = basename(sys.argv[0])
	name = prog.split('.')[0]
	stamp = '%F.%T'
	logln = '%(asctime)s,%(msecs)d %(name)s:%(levelname)s:%(funcName)s %(message)s'
	outln = '%(asctime)s %(name)s: %(message)s'
	_file = expanduser('~/log/%s.log'%name)
	if lvl == ('CRITICAL', 50):
		lvl = logging.CRITICAL
	elif lvl in ('DEBUG', 10):
		lvl = logging.DEBUG
	elif lvl == ('ERROR', 40):
		lvl = logging.ERROR
	elif lvl in ('INFO', 20):
		lvl = logging.INFO
	elif lvl in ('NOTSET', None, 0):
		lvl = logging.NOTSET
	elif lvl in ('WARNING', 30):
		lvl = logging.WARNING
	log = logging.getLogger(name)
	log.setLevel(lvl)
	ch = logging.StreamHandler()
	ch.setLevel(lvl)
	ch.setFormatter(logging.Formatter(outln, datefmt=stamp))
	fh = logging.FileHandler(_file)
	fh.setLevel(lvl)
	fh.setFormatter(logging.Formatter(logln, datefmt=stamp))
	log.addHandler(ch)
	log.addHandler(fh)
	return log


def debug():
	log = logger()
	return log.debug
