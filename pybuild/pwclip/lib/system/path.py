from os import getcwd, chdir, walk, readlink, listdir
from os.path import expanduser, islink, \
    isfile, isdir, abspath, join as pathjoin
import inspect
from stat import S_ISSOCK as _ISSOCK
from configparser import ConfigParser as _ConfPars
from json import load as _jsonload

from system.random import randin

def absrelpath(path, base=None):
	base = base if base else getcwd()
	path = path.strip("'")
	path = path.strip('"')
	if path.startswith('~'):
		path = expanduser(path)
	if islink(path):
		path = readlink(path)
	if '..' in path or not path.startswith('/'):
		pwd = getcwd()
		chdir(base)
		path = abspath(path)
		chdir(pwd)
	return path.rstrip('/')

def realpaths(pathlist, base=None):
	base = base if base else getcwd()
	paths = []
	for path in pathlist:
		if isinstance(path, (list, tuple)):
			#print('list/tuple')
			for pat in path:
				paths = [absrelpath(p, base) for p in path]
		elif isinstance(path, str):
			if ' ' in path:
				#print('liststring')
				paths = [absrelpath(p.strip(), base) for p in path.strip('[]').split(',')]
				break
			else:
				#print('string', path)
				paths.append(absrelpath(path, base))
	return paths

def confpaths(paths, conf, base=''):
	return list(set(['%s/%s/%s' %(expanduser('~'), path[2:], conf) \
        for path in paths if path.startswith('~/') and \
        isfile('%s/%s/%s'%(expanduser('~'), path[2:], conf))] + \
        ['%s/%s/%s' %(base, path[2:], conf) for path in \
        paths if path.startswith('./') and \
        isfile('%s/%s/%s'%(base, path[2:], conf))] + \
        ['%s/%s/%s' %(base, path, conf) for path in paths if not \
        path.startswith('/') and not path.startswith('.') and \
        isfile('%s/%s/%s' %(base, path, conf))] + \
        ['%s/%s' %(path, conf) for path in paths if path.startswith('/') and \
        isfile('%s/%s' %(path, conf))]))

def confdats(*confs):
	cfg = _ConfPars()
	confdats = {}
	for conf in confs:
		cfg.read(conf)
		for section in cfg.sections():
			confdats[section] = dict(cfg[section])
	return confdats

def jconfdats(*confs):
	confdats = {}
	for conf in confs:
		with open(conf, 'r') as stream:
			for (key, val) in _jsonload(stream).items():
				confdats[key] = val
	return confdats

def unsorted(files):
	rands = []
	for i in range(0, len(files)):
		newrand = randin(len(files))
		if newrand in rands:
			continue
		yield files[newrand]

def filesiter(folder, random=False):
	for (d, _, fs) in walk(absrelpath(folder)):
		orderd = sorted if not random else unsorted
		for f in orderd(fs):
			yield pathjoin(d, f)

def findupperdir(path, name):
	while len(path.split('/')) > 1:
		trg = '%s/%s'%(path, name)
		if isdir(trg):
			return trg
		return findupperdir('/'.join(p for p in path.split('/')[:-1]), name)
