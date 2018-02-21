#!/usr/bin/env /usr/bin/python3
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""
blogger module - provides breitlogger class which writes
(timestamped) text to a log file
"""
import os
import sys
#from cmd2 import Cmd

from system import stamp
from executor import command as c
from colortext import bgre, tabd
from colortext import bgre, tabd

class BreitLogger(object):
	dbg = False
	def __init__(self):
		if self.dbg:
			print(bgre(BreitLogger.__mro__))
			print(bgre(tabd(BreitLogger.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
'''
class BreitLogger(): #Cmd):
	"""breitlogger main class"""
	__me = os.uname()[1]
	intro = 'BreitLogger - write timestamped text to file\n'
	logfile = '%s/log/%s-%s.log'%(
	    os.path.expanduser('~'),
	    __me.split('.')[0],
	    stamp().split('.')[0])
	prompt = '%s %s>> '%(__me.split('.')[0], stamp().split('.')[1])
	case_insensitive = False
	dbg = True

	def func_named(self, arg):
		#/usr/lib/python3/dist-packages/cmd2.py
		"""
		overriding cmd2.Cmd.func_named function to fix case senitive I/O which
		unfortunatly breaks with setting case_insensitive to True in the main
		loop (Cmd.cmdloop())
		"""
		result = None
		target = 'do_' + arg
		if target in dir(self):
			result = target
		else:
			if self.abbrev:
				funcs = [
					fname for fname in self.keywords if fname.startswith(
						arg[0])
					]
			if len(funcs) > 0:
				result = 'do_' + funcs[0]
		return result

	def do_last(self, n):
		with open(self.logfile, 'r') as f:
			lines = f.readlines()
			if len(lines) < 10:
				n = len(lines)
			if not n:
				n = 10
			for line in lines[-10:]:
				print('\t', line.strip())

	def do_edit(self, args):
		vicmd = '%s %s'%(which('vim'), self.logfile)
		c.call(vicmd.split(' '))

	def do_ed(self, args):
		self.do_edit(args)

	def do_dl(self, line):
		with open(self.logfile, 'r') as f:
			newfile = '\n'.join(
				line for line in f.readlines()[:-1] if line != '\n')
		with open(self.logfile, 'w+') as f:
			f.write(newfile)

	def default(self, line):
		line = eval(line.split(' ')[0])[0]+' '+' '.join(
			word for word in line.split(' ')[1:])
		with open(self.logfile, 'a') as f:
			f.write('%s>> %s\n'%(stamp(), line.strip()))

	def postparsing_postcmd(self, stop):
		setattr(
		    self, 'prompt',
		    '%s %s>> '%(__me__.split('.')[0], stamp().split('.')[1]))
		return stop
'''







if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
