#!/usr/bin/env /usr/bin/python3
#
# This file is free software by  <- d0n - d0n@janeiskla.de ->
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
"""module disclaimer"""
# global imports
import os
import sys
import socket
import struct
from random import randint

# local relative imports
from net.mac import mac

# global default variables
__version__ = '0.0'


class DHCPDiscover(object):
	_dbg = False
	id_ = b''
	for i in range(4):
		rnd = randint(0, 255)
		id_ += struct.pack('!B', rnd)
	_iface = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # iface <str>
	def iface(self):
		return self._iface
	@iface.setter
	def iface(self, val):
		self._iface = val if type(val) is str else self._iface

	def _packet(self, iface=None):
		if not iface:
			iface = self.iface
		macb = mac(iface, byte=True)
		packet = b''
		# message type: boot request (1)
		packet += b'\x01'
		# hardware type: ethernet
		packet += b'\x01'
		# hardware address length: 6
		packet += b'\x06'
		# hops: 0
		packet += b'\x00'
		# transaction
		packet += self.id_
		# seconds elapsed: 0
		packet += b'\x00\x00'
		# bootp flags: 0x8000 (broadcast) + reserved flags
		packet += b'\x80\x00'
		# client ip address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'
		# your (client) ip address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'
		# next server ip address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'
		# relay agent ip address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'
		# client hw (mac) address
		packet += macb
		# client hardware address padding: 00000000000000000000
		packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		# server host name not given
		packet += b'\x00'*67
		# boot file name not given
		packet += b'\x00'*125
		# magic cookie: dhcp
		packet += b'\x63\x82\x53\x63'
		# option: (t=53,l=1) dhcp message type = dhcp discover
		packet += b'\x35\x01\x01'
		# option: (t=61,l=6) client identifier
		# packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'
		packet += b'\x3d\x06'+macb
		# option: (t=55,l=3) parameter request list
		packet += b'\x37\x03\x03\x01\x06'
		# end option
		packet += b'\xff'
		return packet

	def _discovery(self, timeout=5, packet=None):
		if not packet:
			packet = self._packet()
		dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		dhcps.bind(('', 68))
		dhcps.setblocking(0)
		dhcps.sendto(packet, ('<broadcast>', 67))
		dhcps.settimeout(timeout)
		try:
			while True:
				return dhcps.recv(1024)
		finally:
			dhcps.close()

	def discover(self, data=None):
		if not data:
			data = self._discovery()
		if data[4:8] == self.id_:
			ipoffer = '.'.join(map(lambda x:str(x), data[16:20]))
			server = '.'.join(map(lambda x:str(x), data[245:249]))
			lease = str(struct.unpack('!L', data[251:255])[0])
			netmask = int(data[268]/4)
			for i in range(0, 4 * netmask, 4):
				netmask = '.'.join(map(
				    lambda x:str(x), data[269 + i :269 + i + 4]))
		return {
		    'server': server, 'ipoffer': ipoffer,
		    'netmask': netmask, 'lease': lease
		    }



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(m for m in dir()))
	dhcp = DHCPDiscover(**{'iface':'eth0'})
	print(dhcp.discover())
