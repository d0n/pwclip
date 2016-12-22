#!/usr/bin/env python3
"""module disclaimer"""

# global imports
import re
from os import readlink, path
import sys
import psutil
from time import sleep

# local relative imports
from executor import Command, sucommand as sudo
from system import which, absrelpath
from net.iface import ifaces, ifaddrs
from colortext import bgre, abort, error

# default vars
__version__ = '0.1'

class VPNConfig(Command):
	_sh_ = True
	_su_ = True
	_pid = None
	_ocbin = which('openconnect')
	_pidfile = '/run/openconnect.pid'
	dbg = False
	vpncfgs = {
        'ifname': 'tun0',
        'keystore': '~/.vpn'}
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self._dbg:
			print(VPNConfig.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)

	@property               # pidfile <str>
	def pidfile(self):
		return self._pidfile
	@pidfile.setter
	def pidfile(self, val):
		self._pidfile = val
		if val and not val.startswith('/'):
			self._pidfile = '/run/%s.pid'%val

	@property                # pid <int>
	def pid(self):
		try:
			with open(self.pidfile, 'r') as pfh:
				return int(pfh.read())
		except FileNotFoundError:
			pass

	@property               # ocbin <str>
	def ocbin(self):
		return self._ocbin

	@staticmethod
	def _vpnpath(vpnfile, vpndir='~/.vpn'):
		return '%s/%s'%(path.expanduser(vpndir), vpnfile)

	def vpnstatus(self):
		if self.dbg:
			print(bgre(self.vpnstatus))
		if self.pid:
			proc = psutil.Process(self.pid)
			if proc.is_running():
				return True

	def connect(self):
		if self.dbg:
			print(bgre(self.connect))
		vpndir = self.vpncfgs['keystore']
		occmd = '%s --no-xmlpost -b -q --pid-file=%s ' \
            '--certificate=%s --sslkey=%s --cafile=%s --user=%s %s'%(
                self.ocbin, self.pidfile,
                self._vpnpath(self.vpncfgs['cert'], vpndir),
                self._vpnpath(self.vpncfgs['key'], vpndir),
                self._vpnpath(self.vpncfgs['office'], vpndir),
                self.vpncfgs['user'],  self.vpncfgs['gate'])
		try:
			return (self.call(occmd) == 0)
		except KeyboardInterrupt:
			try:
				abort()
			except PermissionError as err:
				error(err)
		except PermissionError:
			abort()

	def reconnect(self):
		"""SIGUSR2"""
		pass

	def disconnect(self):
		if self.dbg:
			print(bgre(self.disconnect))
		ocpid = None
		if path.isfile('/var/run/%s'%(self.pidfile)):
			with open('/var/run/%s'%(self.vpncfgs['pidfile']), 'r') as f:
				ocpid = str(f.read()).strip()
		if not ocpid:
			ocpid = self.stdx('pidof '+self.ocbin).strip()
		if ocpid:
			try:
				return (self.erno('kill -SIGINT %s'%ocpid) == 0)
			except KeyboardInterrupt:
				abort()
			except PermissionError as err:
				error(err)

	def switch(self):
		if self.dbg:
			print(bgre(self.switch))
		if self.vpnstatus():
			if self.disconnect():
				return 'disconnected'
		else:
			if self.connect():
				return 'connected'








if __name__ == '__main__':
	#display all classes/definitions which are imported/defined (disabled)
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
