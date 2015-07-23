import os
import inspect

def realpaths(*pathlist, base=os.getcwd()):
	#print(pathlist, base)
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
		return path.rstrip('/')
	paths = []
	for path in pathlist:
		if isinstance(path, list) or isinstance(path, tuple):
			print('list/tuple')
			for pat in path:
				paths = paths + [_absrelpath(p) for p in path]
		elif isinstance(path, str):
			if ' ' in path:
				print('liststring')
				paths = paths + [_absrelpath(p.strip()) for p in path.strip('[]').split(',')]
			else:
				print('string', path)
				paths.append(_absrelpath(path))
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
