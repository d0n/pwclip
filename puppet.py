#!/usr/bin/env python3
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
"""puppet wrapping module"""

# global imports
import os
import sys

# local relative imports
sys.path = [os.path.expanduser('~/bin')] + [p for p in sys.path if (
    not p == '%s/bin'%(os.path.expanduser('~')))]
from modules.network.common import fqdn, netcat as nc
from modules.network.ssh import SecureSHell
from modules.system.executor import Command
from modules.system.common import which

# global default variables
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))
__version__ = '0.2'

class Puppet(Command):
	"""puppet wrapper class"""
	_sh_ = True
	_dbg = False
	_bgr = False
	_user = 'root'
	_host = ''
	_puptmpl = '%s/puppet.tmpl'%(os.path.expanduser('~/bin/config'))
	scp = SecureSHell().put
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
		if self.dbg:
			print(Puppetti.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # bgr <bool>
	def bgr(self):
		return self._bgr
	@bgr.setter
	def bgr(self, val):
		self._bgr = val if type(val) is bool else self._bgr
	@property               # host <str>
	def host(self):
		return self._host
	@host.setter
	def host(self, val):
		self._host = val if type(val) is str else self._host
	@property               # user <str>
	def user(self):
		return self._user
	@user.setter
	def user(self, val):
		self._user = val if type(val) is str else self._user

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
		    host=fqdn(self.host))[0].split('.')[0]
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
		      'aptitude update', 'aptitude -y full-upgrade',
		      'aptitude install %s puppet lsb-release'%(aptopts)):
			xec(cmd, host=fqdn(self.host))
		self.run(
		    '%s -o User="root" -o StrictHostKeyChecking=no ' \
		    '-o UserKnownHostsFile=/dev/null -o LogLevel=ERROR ' \
		    '%s %s:/etc/puppet/puppet.conf'%(which('scp'),
		    self._puptmpl, fqdn(self.host)))

	def puprun(self, bgr=None):
		"""run puppet agent remotely"""
		if self.dbg:
			print(self.puprun)
		if not bgr:
			bgr = self.bgr
		xec = self.call
		if bgr:
			xec = self.run
		xec('puppet agent -vot', host=fqdn(self.host))













if __name__ == '__main__':
	"""module debugging area"""
	puppet = Puppetti(*('dbg'), **{'host':'accbuildtest01'})
	#print(puppet.puppetrun())
	#puppet.write_puppetconf()
	#print(puppet.delcert('accspptest01'))
	#for ln in puppet.push():
	#	print(ln)
	print(puppet.delssl())
	print(puppet.delcert())
	puppet.write_puppetconf()
	print(puppet.puppetrun())
