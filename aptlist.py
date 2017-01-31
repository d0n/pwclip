#!/usr/bin/env python3
from sys import argv
from os import listdir
from os.path import basename, isfile


"""
deb http://ftp.debian.org/debian jessie main contrib non-free
deb-src http://ftp.debian.org/debian jessie main contrib non-free
"""





class AptListParser(object):
	"""
	deb http://archive.ubuntu.com/ubuntu trusty main restricted universe multiverse
	deb-src http://archive.ubuntu.com/ubuntu trusty main restricted universe multiverse

	deb http://archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse
	deb-src http://archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse

	deb http://archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse
	deb-src http://archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse

	deb http://security.ubuntu.com/ubuntu trusty-security main restricted universe multiverse
	deb-src http://security.ubuntu.com/ubuntu trusty-security main restricted universe multiverse

	deb http://archive.canonical.com/ubuntu trusty partner
	deb-src http://archive.canonical.com/ubuntu trusty partner

	deb http://extras.ubuntu.com/ubuntu trusty main
	deb-src http://extras.ubuntu.com/ubuntu trusty main
    """
	aptlist = '/etc/apt/sources.list'

	def _aptlists(self):
		aptlsts = [self.aptlist] if isfile(self.aptlist) else []
		aptdir = '%s.d'%self.aptlist
		return aptlsts + ['%s/%s'%(
            aptdir, f) for f in listdir(aptdir) if f.endswith('.list')]

	def _listrepos(self, listfiles, ignrepos=[]):
		repolist = []
		for listfile in listfiles:
			if not isfile(listfile): continue
			with open(listfile, 'r') as lst:
				for repo in lst.readlines():
					repo = repo.strip()
					if repo.startswith('#') or \
                          [i for i in ignrepos if i in repo]:
						continue
					repolist.append(repo)
		return repolist

	def aptpars(self):
		for line in self.listrepos(self.aptlists()):
			line = line.strip()
			if line.startswith('#') or not line:
				continue
			src, url, ver, branchs = \
                line.split()[0], line.split()[1], \
                line.split()[2], line.split()[3:]
			print(src, url, ver, branchs)


