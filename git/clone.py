#!/usr/bin/env python3
"""git wrapping module"""
# global imports
import re
import os
from os.path import isfile as _isfile
import sys

# local relative imports
from executor import Command
from system import which
from colortext import blu, yel, bgre

from .repo import GitRepo

# default vars
__version__ = '0.1'

class GitClone(GitRepo):
	user = os.getenv('USER')
	remote = None
	repodir = None
	dbg = None
	def __init__(self, *args, **kwargs):
		if 'debug' in kwargs.keys():
			self.dbg = kwargs['debug']
		if 'remote' in kwargs.keys():
			self.remote = kwargs['remote']
		if 'user' in kwargs.keys():
			self.user = kwargs['user']
		if 'rpodir' in kwargs.keys():
			self.rpodir = kwargs['rpodir']
		if self.dbg:
			print(bgre(GitClone.__mro__))
			print(bgre('user', self.user))
			print(bgre('remote', self.remote))
			print(bgre('repodir', self.rpodir))
			print()

	def clone(self, repo, target=None):
		if self.repodir:
			repo = self.repodir+'/'+repo
		remote = self.user+'@'+self.remote+':'+repo+'.git'
		command = git+' clone '+remote
		if target:
			if not os.path.isdir('/'.join(d for d in target.split('/')[:-1])):
				os.makedirs('/'.join(d for d in target.split('/')[:-1]))
			command = command+' '+target
		if int(self.call(command)) == 0:
			return True












if __name__ == '__main__':
	exit(1)
