#!/usr/bin/env python3
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY! Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# Write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
"""
eththernet interfaces configuration module
"""
# global imports
import os
import sys

# local relative imports
from net.ifdrougs import ifup, ifdown
from system import which
from net.network import ifaces
from colortext import bgre
from pars import NetworkInterfacesParser

# default vars
__version__ = '0.1'

class ETHConfig(NetworkInterfacesParser):
	"""eth base configuration module"""
	_dbg = False
	_iv4 = False
	_iv6 = False
	_dhc = False
	_ato = False
	_cfgs = {}
	_iface = 'eth0'
	_nifconf = '/etc/network/interfaces'
	_dhcconf = '/etc/dhcp/dhclient.conf'
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and type(getattr(self, key)) is not bool:
				setattr(self, key, val)
		if self.dbg:
			print(bgre('%s\n%s\n'%(
			    ETHConfig.__mro__,
			    '\n'.join('  %s%s=\t%s'%(k[1:], ' '*int(
			        int(max(len(i) for i in self.__dict__.keys())+4
			        )-len(k)), v
			    ) for (k, v) in self.__dict__.items()))))
	# rw properties
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # iv4 <bool>
	def iv4(self):
		return self._iv4
	@iv4.setter
	def iv4(self, val):
		self._iv4 = val if type(val) is bool else self._iv4
	@property               # dhc <bool>
	def dhc(self):
		return self._dhc
	@dhc.setter
	def dhc(self, val):
		self._dhc = val if type(val) is bool else self._dhc
	@property               # ato <bool>
	def ato(self):
		return self._ato
	@ato.setter
	def ato(self, val):
		self._ato = val if type(val) is bool else self._ato
	@property               # ifcfgs <dict>
	def cfgs(self):
		return self._cfgs
	@cfgs.setter
	def cfgs(self, val):
		self._cfgs = val if type(val) is dict else self._cfgs
	@property               # iface <str>
	def iface(self):
		return self._iface
	@iface.setter
	def iface(self, val):
		self._iface = val if type(val) is str else self._iface
	@property               # nifconf <str>
	def nifconf(self):
		return self._nifconf
	@nifconf.setter
	def nifconf(self, val):
		self._nifconf = val if type(val) is str else self._nifconf
	@property               # dhcconf <str>
	def dhcconf(self):
		return self._dhcconf
	@dhcconf.setter
	def dhcconf(self, val):
		self._dhcconf = val if type(val) is str else self._dhcconf

	def connect(self, iface=None):
		"""interface up/connect method"""
		if self.dbg:
			print(bgre(self.connect))
		if not iface:
			iface = self.iface
		_, confs = self.read_netconf()
		confds = [c.split()[1] for c in confs if c]
		mode = self.dhc
		if 'mode' in self.cfgs.keys() and self.cfgs['mode'] == 'static':
			config = dict((k, v) for (k, v) in self.cfgs.items() if not k == 'mode')
			mode = 'static'
		else:
			config = dict((k, v) for (k, v) in self.cfgs.items() if not k == 'mode')
		if not iface in confds:
			self.write_netconf(iface, mode=mode, auto=self.ato, config=config)
		if ifup(iface, dhcp=self.dhc):
			return iface

	def disconnect(self, iface):
		"""disconnection method"""
		if self.dbg:
			print(bgre(self.disconnect))
		if ifdown(iface):
			return True






if __name__ == '__main__':
	"""debugging area for modules"""
	"""
	for func in dir(sys.modules[__name__]):
		if not '-v' in sys.argv:
			if str(func).startswith('__') or func == 'func':
				continue
		print(func)
		if func in sys.argv:
			print(dir(func))
			continue
	print()
	"""
	eth = ETHConfig(*('ip4', 'dhc', 'dbg', 'frc'), **{'eth1': {'ip': '22.2.2.2/16'}})
	eth.connect()
