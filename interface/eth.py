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
from system import which
from colortext import bgre, tabd
from pars.network import NetworkInterfacesParser
from net.iface import ifaces
from net.util.ifdrougs import ifup, ifdown

class ETHConfig(NetworkInterfacesParser):
	"""eth base configuration module"""
	dbg = False
	iv4 = False
	iv6 = False
	dhc = False
	ato = False
	cfgs = {}
	iface = 'eth0'
	nifconf = '/etc/network/interfaces'
	dhcconf = '/etc/dhcp/dhclient.conf'
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key) and type(getattr(self, key)) is not bool:
				setattr(self, key, val)
		if self.dbg:
			print(bgre(ETHConfig.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

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
