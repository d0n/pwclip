from os.path import \
    expanduser as _expanduser

from yaml import \
    load as _load

import logging as _log
from logging.config import \
    dictConfig as _logconf

def _log_(name):
	with open(_expanduser('~/.config/pylogger.yaml'), 'r') as yml:
		cfgs = _load(yml)
	_logconf(cfgs)
	return _log.getLogger(name)
