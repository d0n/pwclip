# -*- coding: utf-8 -*-
from os import path, walk, makedirs, chdir, stat, chmod

from shutil import rmtree

import yaml

def writepathyaml(target, yamlfile=None):
	yamlfile = yamlfile if yamlfile else '%s.yaml'%target
	chdir(target)
	yml = {}
	for (d, _, fs) in walk('.'):
		for f in fs:
			f = '%s/%s'%(d, f)
			with open(f, 'rb') as ffh:
				yml[f] = [ffh.read(), stat(f).st_mode]
	with open(ymlf, 'w+') as yfh:
		yfh.write(yaml.dump(yml))

def readpathyaml(yamlfile, target=None):
	with open(yamlfile, 'r') as yfh:
		yml = yaml.load(yfh.read())
	target = target if target else '.'
	try:
		makedirs(target)
	except FileExistsError:
		pass
	chdir(target)
	for (f, ds) in yml.items():
		try:
			makedirs(path.dirname(f))
		except FileExistsError:
			pass
		with open(f, 'wb+') as ffh:
			ffh.write(ds[0])
		chmod(f, int(ds[1]))

