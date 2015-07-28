import os
import inspect


def absrelpath(path, base=os.getcwd()):
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
	return path.rstrip('/')


def realpaths(*pathlist, base=os.getcwd()):
	#print(pathlist, base)
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
				paths.append(absrelpath(path), base)
	if paths:
		if len(paths) > 1:
			return paths
		return paths[0]

def confpaths(paths, conf, base=os.getcwd()):
	#print('%s\n%s\n%s'%(paths, conf, base))
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
	from configparser import ConfigParser as _ConfPars
	cfg = _ConfPars()
	confdats = {}
	for conf in confs:
		cfg.read(conf)
		for section in cfg.sections():
			confdats[section] = dict(cfg[section])
	return confdats

def jconfdats(*confs):
	from json import load as _load
	confdats = {}
	for conf in confs:
		with open(conf, 'r') as stream:
			for (key, val) in _load(stream).items():
				confdats[key] = val
	return confdats
