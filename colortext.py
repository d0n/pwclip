#!/usr/bin/python3
import sys

# get color escape sequence from string
def __colorize(color, text):
	string = '\033['
	if len(color) == 4:
		color = color[1:]
		string = '%s01;'%(string)
	if color == 'gre':
		string = '%s30m'%(string)
	if color == 'red':
		string = '%s31m'%(string)
	if color == 'grn':
		string = '%s32m'%(string)
	if color == 'yel':
		string = '%s33m'%(string)
	if color == 'blu':
		string = '%s34m'%(string)
	if color == 'vio':
		string = '%s35m'%(string)
	if color == 'cya':
		string = '%s36m'%(string)
	if color == 'whi':
		string = '%s37m'%(string)
	colortext = '%s%s\033[0m'%(string, text)
	return colortext

# define 2 functions for each color
# one for normal and one for bold text

def blu(text):
	#func = sys._getframe().f_code.co_name
	return __colorize('blu', text)
def bblu(text):
	return __colorize('bblu', text)

def cya(text):
	return __colorize('cya', text)
def bcya(text):
	return __colorize('bcya', text)

def gre(text):
	return __colorize('gre', text)
def bgre(text):
	return __colorize('bgre', text)

def grn(text):
	return __colorize('grn', text)
def bgrn(text):
	return __colorize('bgrn', text)

def red(text):
	return __colorize('red', text)
def bred(text):
	return __colorize('bred', text)

def vio(text):
	return __colorize('vio', text)
def bvio(text):
	return __colorize('bvio', text)

def whi(text):
	return __colorize('whi', text)
def bwhi(text):
	return __colorize('bwhi', text)

def yel(text):
	return __colorize('yel', text)
def byel(text):
	return __colorize('byel', text)

# functions for some high frequent use cases:
def error(*args, **kwargs):
	'''
	while i most often want to display error texts which heave
	one or more primary causes i want the text parts printed
	in red and the causes printed in yellow as follows
	'''
	#sys.stdout.flush()
	#sys.stderr.flush()
	errfile = ''
	errline = ''
	buzzword = 'ERROR:'
	if 'file' in kwargs.keys():
		errfile = '%s:'%(kwargs['file'])
	if 'line' in kwargs.keys():
		errline = '%s:'%(kwargs['line'])
	if 'warn' in kwargs.keys():
		buzzword = 'WARNING:'
	msgs = [errfile+errline+red(buzzword)]
	for arg in args:
		if (args.index(arg) % 2) == 0:
			msgs.append(red(arg))
		else:
			msgs.append(yel(arg))
	print(' '.join(msg for msg in msgs), flush=True)
	#sys.stdout.flush()
	#sys.stderr.flush()


def fatal(*args, **kwargs):
	'''
	does exactly the same as "error" except it prints texts
	in bold and kills its parent processes
	'''
	#sys.stdout.flush()
	#sys.stderr.flush()
	errfile = ''
	errline = ''
	if 'file' in kwargs.keys():
		errfile = '%s:'%(kwargs['file'])
	if 'line' in kwargs.keys():
		errline = '%s: '%(kwargs['line'])
	msgs = ['%s%s%s'%(errfile, errline, bred('FATAL:'))]
	for arg in args:
		if (args.index(arg) % 2) == 0:
			msgs.append(bred(arg))
		else:
			msgs.append(yel(arg))
	print(' '.join(msg for msg in msgs), flush=True)
	#sys.stdout.flush()
	#sys.stderr.flush()
	exit(1)

def abort(*messages):
	if not messages:
		messages = ('\naborted by keystroke', )
	'''
	prints all text in blu by using STDOUT but also kills its
	parent processes and returns 0 (OK) instead of 1 (ERROR)
	by default used for aborting on STRG+C (see message,
	for "KeyboardInterrupt" exceptions)
	'''
	msgs = []
	for msg in messages:
		if (messages.index(msg) % 2) == 0:
			msgs.append(blu(msg))
		else:
			msgs.append(yel(msg))
	print(' '.join(msg for msg in msgs), flush=True)
	#sys.stdout.flush()
	exit(0)

def tabd(keyvals):
	if not type(keyvals) is dict:
		raise TypeError('cannot process type %s expected dict'%type(keyvals))
	tabbed = ''
	lim = max(len(k) for k in keyvals.keys())+4
	for (key, val) in sorted(keyvals.items()):
		tabbed = '%s%s%s= %s\n'%(tabbed, key, ' '*int(lim-len(key)), val)
	return tabbed.strip()



if __name__ == "__main__":
	# module debugging area
	print('\n'.join(m for m in dir()))
