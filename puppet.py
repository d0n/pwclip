#!/usr/bin/env python3
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
"""puppet wrapping module"""

# global imports
from os.path import expanduser
import sys
from socket import getfqdn as fqdn
from paramiko.ssh_exception import AuthenticationException

# local relative imports
from colortext import bgre, tabd
from system import which
from net import netcat as nc, SecureSHell as SSH

class Puppet(SSH):
	"""puppet wrapper class"""
	sh_ = True
	dbg = False
	vrb = False
	bgr = False
	reuser = 'root'
	remote = ''
	puptenv = 'accmo_master'
	puptmpl = '~/.config/amt/puppet.tmpl'
	pupconf = '/etc/puppetlabs/puppet/puppet.conf'
	pupdpkg = 'puppet-agent'
	ppcasrv = 'puppet-access-ca.server.lan'
	ppsysrv = 'puppet-access-sync.server.lan'
	pupvers = 4
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '%s_'%key):
				setattr(self, '%s_'%key, val)
		self.remote = fqdn(self.remote)
		try:
			if self._debversion() < '8':
				self.pupvers = 2
				self.puptmpl = '~/.config/amt/puppet2.tmpl'
				self.pupconf = '/etc/puppet/puppet.conf'
				self.pupdpkg = 'puppet'
				self.puptenv = 'itoacclive'
				self.ppcasrv = 'puppetca.dlan.cinetic.de'
				self.ppsysrv = 'puppetsync.server.lan'
		except AuthenticationException:
			pass
		if self.dbg:
			print(bgre(Puppet.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		SSH.__init__(self, *args, **kwargs)

	def _debversion(self):
		if self.dbg:
			print(self._debversion)
		return list(str(self.rstdo(
              'cat /etc/debian_version', remote=self.remote
              )).split('.'))[0]

	def pupush(self):
		"""push current svn revision to puppet master"""
		if self.dbg:
			print(self.pupush)
		return nc(self.ppsysrv, '18140', self.puptenv)

	def pupcrt(self):
		"""remove puppet ssl certificates on puppetca"""
		if self.dbg:
			print(self.pupcrt)
		cmd = 'certclean' if self.pupvers == 4 else 'cert clean'
		msg = '%s %s'%(cmd, self.remote)
		print(self.ppcasrv, msg)
		return nc(self.ppcasrv, '8140', self.remote)

	def pupssl(self):
		"""remove puppet ssl certificates remotely"""
		if self.dbg:
			print(self.pupssl)
		if self.pupvers == 2:
			if self.rcall(
                  'rm -rf /var/lib/puppet/ssl/',
                  remote=fqdn(self.remote)) == 0:
				return True
		if self.rcall(
              'rm -rf /etc/puppetlabs/puppet/ssl',
              remote=fqdn(self.remote)) == 0:
			return True


	def pupini(self, background=None):
		"""puppet writing method by using template"""
		if self.dbg:
			print(self.pupini)
		if not background:
			background = self.bgr
		xec = self.rcall
		if background:
			xec = self.rrun
		aptopts = '-y'
		cmds = [
            'apt-get update', 'apt-get -y upgrade',
            'apt-get install -y lsb-release %s'%self.pupdpkg]
		for cmd in cmds:
			xec(cmd, remote=fqdn(self.remote))
		self.put(expanduser(self.puptmpl), self.pupconf,
            remote=self.remote, reuser=self.reuser)

	def puprun(self, bgr=None):
		"""run puppet agent remotely"""
		if self.dbg:
			print(bgre(self.puprun))
		if not bgr:
			bgr = self.bgr
		xec = self.rcall
		if bgr:
			xec = self.rrun
		cmd = 'PATH=$PATH:/opt/puppetlabs/bin puppet agent -vot'
		if self.dbg:
			cmd = 'PATH=$PATH:/opt/puppetlabs/bin puppet agent -vot --debug'
		xec(cmd, remote=fqdn(self.remote))













if __name__ == '__main__':
	exit(1)
	#
	# module debugging area
	#
	#puppet = Puppet(*('dbg'), **{'host':'accbuildtest01'})
	#print(puppet.puppetrun())
	#puppet.write_puppetconf()
	#print(puppet.delcert('accspptest01'))
	#for ln in puppet.push():
	#	print(ln)
	#print(puppet.delssl())
	#print(puppet.delcert())
	#puppet.write_puppetconf()
	#print(puppet.puppetrun())
