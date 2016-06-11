#!/usr/bin/env python3
"""common system functions module"""
# global imports
import re
import os
import sys
import inspect
import types
# default vars
__version__ = '1.0'

def whoami():
	with open('/etc/passwd', 'r') as pwf:
		pwl = pwf.readlines()
	user = [u.split(':')[0] for u in pwl if u.split(':')[2] == os.getuid()]
	if user:
		return user[0]

def bestlim(*strings):
	return max(len(s) for s in strings)+4

def lineno():
	return inspect.currentframe().f_back.f_lineno

def which(prog):
	for path in os.environ['PATH'].split(':'):
		if os.access('%s/%s'%(path, prog), os.X_OK):
			return '%s/%s'%(path, prog)

def random(limit=10, pattern='[\w -~]'):
	rnds = ''
	while len(rnds) < int(limit):
		try:
			out = os.urandom(1)
			out = out.decode()
		except UnicodeDecodeError as err:
			continue
		char = re.search(r'%s'%(pattern), out, re.U)
		if char:
			rnds = '%s%s'%(rnds, out.strip())
			#rnds = rnds.strip()
	return rnds

def string2bool(varstr):
	varstr = str(varstr).lower()
	if varstr in ('false', 'disabled', '0'):
		return False
	elif varstr in ('true', 'enabled', '1'):
		return True
	elif varstr in ('none', '', [], {}):
		return None
	else:
		return varstr
