import sys
from os import getuid
from os.path import \
    basename, expanduser, isdir

from yaml import \
    load

from logging import \
    basicConfig, getLogger, INFO

def logger(name):
	logdir = '/var/log/%s'%name
	if getuid() != 0:
		logdir = expanduser('~/log/%s'%name)
	logfile = '%s/%s.log'%(logdir, name)
	if not isdir(logdir):
		makedirs(logdir)
	basicConfig(
        format='%(asctime)s,%(msecs)03d ' \
            '%(levelname)s %(funcName)s - %(message)s',
        level=INFO, filename=logfile, datefmt='%F.%T')
	return getLogger(logfile)

def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    if len(root.handlers) == 0:
        basicConfig()
    msg = '\033[01;30m%s\033[0m'%msg
    root.debug(msg, *args, **kwargs)

