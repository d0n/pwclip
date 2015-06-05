import os
import inspect
from configparser import ConfigParser

def bestlim(*strings):
	return max(len(s) for s in strings)+4

def lineno():
	return inspect.currentframe().f_back.f_lineno

def realpaths(*pathlist, base=os.getcwd()):
	def _absrelpath(path):
		path = path.strip("'")
		path = path.strip('"')
		if path.startswith('~'):
			path = os.path.expanduser(path)
		if os.path.islink(path):
			path = os.readlink(path)
		if '..' in path or not path.startswith('/'):
			pwd = os.getcwd()
			os.chdir(base)
			path = os.path.abspath(path)
			os.chdir(pwd)
		return path
	for paths in pathlist:
		if type(paths) in (list, tuple):
			for path in paths:
				paths = [_absrelpath(path) for path in paths]
		else:
			paths = _absrelpath(paths)
	return paths


def confpaths(paths, conf, base=os.getcwd()):
	return list(set(['%s/%s/%s' %(os.path.expanduser('~'), path[2:], conf) \
    for path in paths if path.startswith('~/') and \
    os.path.isfile('%s/%s/%s'%(os.path.expanduser('~'), path[2:], conf))] + \
    ['%s/%s/%s' %(base, path[2:], conf) for path in \
    paths if path.startswith('./') and \
    os.path.isfile('%s/%s/%s'%(base, path[2:], conf))] + \
    ['%s/%s/%s' %(base, path, conf) for path in paths if not \
    path.startswith('/') and not path.startswith('.') and \
    os.path.isfile('%s/%s/%s' %(base, path, conf))] + \
    ['%s/%s' %(path, conf) for path in paths if path.startswith('/') and \
    os.path.isfile('%s/%s' %(path, conf))]))

def confdats(*confs):
	cfg = ConfigParser()
	confdats = {}
	for conf in confs:
		cfg.read(conf)
		for section in cfg.sections():
			confdats[section] = dict(cfg[section])
	return confdats

