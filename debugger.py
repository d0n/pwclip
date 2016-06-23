from sys import \
    argv as _argv
from os.path import \
    basename as _basename, \
    expanduser as _expanduser
from yaml import \
    load as _load
import logging

def debug():
	prog = _basename(_argv[0])
	name = prog.split('.')[0]
	stamp = '%F.%T'
	logln = '%(asctime)s,%(msecs)d %(name)s:%(levelname)s:%(funcName)s %(message)s'
	outln = '%(asctime)s %(name)s: %(message)s'
	_file = _expanduser('~/log/%s.log'%name)
	log = logging.getLogger(name)
	log.setLevel(logging.DEBUG)

	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(logging.Formatter(outln, datefmt=stamp))

	fh = logging.FileHandler(_file)
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(logging.Formatter(logln, datefmt=stamp))

	log.addHandler(ch)
	log.addHandler(fh)
	return log.debug
