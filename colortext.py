#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
text colorisation functions - due to extendet use of the python3 print
function this is for python3 only
"""
from sys import \
    stderr as _stderr

# get color escape sequence from string
def __colorize(color, text):
	"""color-tag prepending and end-tag appending function"""
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
	"""function for color blue"""
	#import sys
	#func = sys._getframe().f_code.co_name
	return __colorize('blu', text)
def bblu(text):
	"""function for color bold-blue"""
	return __colorize('bblu', text)

def cya(text):
	"""function for color cyan"""
	return __colorize('cya', text)
def bcya(text):
	"""function for color bold-cyan"""
	return __colorize('bcya', text)

def gre(text):
	"""function for color grey"""
	return __colorize('gre', text)
def bgre(text):
	"""function for color bold-grey"""
	return __colorize('bgre', text)

def grn(text):
	"""function for color green"""
	return __colorize('grn', text)
def bgrn(text):
	"""function for color bold-green"""
	return __colorize('bgrn', text)

def red(text):
	"""function for color red"""
	return __colorize('red', text)
def bred(text):
	"""function for color bold-red"""
	return __colorize('bred', text)

def vio(text):
	"""function for color violet"""
	return __colorize('vio', text)
def bvio(text):
	"""function for color bold-violet"""
	return __colorize('bvio', text)

def whi(text):
	"""function for color white"""
	return __colorize('whi', text)
def bwhi(text):
	"""function for color bold-white"""
	return __colorize('bwhi', text)

def yel(text):
	"""function for color guess what? - yellow ;)"""
	return __colorize('yel', text)
def byel(text):
	"""function for color and you already guessed it... bold-yellow"""
	return __colorize('byel', text)

# functions for some high frequent use cases:
def abort(*messages):
	"""
	prints all text in blu by using STDOUT but also kills its
	parent processes and returns 0 (OK) instead of 1 (ERROR)
	by default used for aborting on STRG+C (see message,
	for "KeyboardInterrupt" exceptions)
	"""
	if not messages:
		messages = ('\naborted by keystroke', )
	msgs = []
	for msg in messages:
		if (messages.index(msg) % 2) == 0:
			msgs.append(blu(msg))
		else:
			msgs.append(yel(msg))
	print(' '.join(msg for msg in msgs), flush=True)
	exit(1)

def error(*args, **kwargs):
	'''
	while i most often want to display error texts which heave
	one or more primary causes i want the text parts printed
	in red and the causes printed in yellow as follows
	'''
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
	print(' '.join(msg for msg in msgs), flush=True, file=_stderr)



def fatal(*args, **kwargs):
	'''
	does exactly the same as "error" except it prints texts
	in bold and kills its parent processes
	'''
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
	print(' '.join(msg for msg in msgs), flush=True, file=_stderr)
	exit(1)

def tabd(keyvals, add=2):
	"""
	this is a function where i try to guess the best indentation for text
	representation of key-value paires with best matching indentation
	e.g:
	foo         = bar
	a           = b
	blibablubb  = bla
	^^indent "bar" and "b" as much as needed ("add" is added to each length)
	"""
	if not isinstance(keyvals, dict):
		raise TypeError('cannot process type %s expected dict'%type(keyvals))
	tabbed = ''
	lim = max(len(k) for k in keyvals.keys())+int(add)
	for (key, val) in sorted(keyvals.items()):
		tabbed = '%s%s%s= %s\n'%(tabbed, key, ' '*int(lim-len(key)), val)
	return tabbed.strip()



if __name__ == "__main__":
	# module debugging area
	#print('\n'.join(m for m in dir()))
	exit(1)
