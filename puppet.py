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
import os
import sys
from socket import getfqdn as fqdn

# local relative imports
from colortext import bgre, tabd
from system import which
from net import netcat as nc, SecureSHell
from executor import SSHCommand

# global default variables
__me__ = os.path.basename(sys.argv[0]).split('.')[0]
__version__ = '0.2'

class Puppet(SSHCommand):
	"""puppet wrapper class"""
	sh_ = True
	dbg = False
	vrb = False
	bgr = False
	user_ = 'root'
	host_ = ''
	_template = '~/.config/puppet.tmpl'
	scp = SecureSHell()
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '%s_'%key):
				setattr(self, '%s_'%key, val)
		if self.dbg:
			print(bgre(Puppet.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	def pupush(self):
		"""push current svn revision to puppet master"""
		if self.dbg:
			print(self.pupush)
		return nc('puppetsync.server.lan', '18140', 'itoacclive')

	def pupcrt(self):
		"""remove puppet ssl certificates on puppetca"""
		if self.dbg:
			print(self.pupcrt)
		return nc('puppetca.dlan.cinetic.de', '18140', fqdn(self.host))

	def pupssl(self):
		"""remove puppet ssl certificates remotely"""
		if self.dbg:
			print(self.pupssl)
		if self.call(
              'rm -rf /var/lib/puppet/ssl/',
              host=fqdn(self.host)) == 0:
			return True

	def pupini(self, background=None):
		"""puppet writing method by using template"""
		if self.dbg:
			print(self.pupini)
		if not background:
			background = self.bgr
		xec = self.call
		if background:
			xec = self.run
		debver = self.stdo(
            'cat /etc/debian_version',
            host=self.host)
		debver = debver[0].split('.')[0]
		aptopts = '-y'
		if debver and debver == '6':
			bprpo = self.stdo(
                'grep -r "squeeze-backports" "/etc/apt/sources.list.d"',
                host=fqdn(self.host))
			if not bprpo:
				xec(
                    'echo "deb http://debian.schlund.de/debian-backports ' \
                    'squeeze-backports main contrib non-free" > ' \
                    '/etc/apt/sources.list.d/debian-backports.list',
                    host=fqdn(self.host))
			aptopts = '-y -t squeeze-backports'
		for cmd in (
              'apt-get update', 'apt-get -y upgrade',
              'apt-get install -y puppet lsb-release'): # %(aptopts)):
			xec(cmd, host=fqdn(self.host))
		#print(self._template, '/etc/puppet/puppet.conf')
		self.scp.put(
            os.path.expanduser(self._template),
            '/etc/puppet/puppet.conf', host=fqdn(self.host), user='root')

	def puprun(self, bgr=None):
		"""run puppet agent remotely"""
		if self.dbg:
			print(self.puprun)
		if not bgr:
			bgr = self.bgr
		xec = self.call
		if bgr:
			xec = self.run
		xec('puppet agent -vot', host=fqdn(self.host_))













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
