#!/usr/bin/env python3
"""wlan connectivity module"""

# global imports
import os
import sys

# local relative imports
from net.iface import isup, ifaces, isconfd, anyifconfd
from system import fileage, which
from executor import sucommand
from colortext import bgre
from pars import NetworkInterfacesParser

from net.util.ifdrougs import ifup, ifdown, ifconfup, ifconfdown

# default vars
__version__ = '0.2'

class WLANConfig(NetworkInterfacesParser):
	_sh_ = True
	_dbg = False
	_prs = False
	_iface = 'wlan0'
	_wpaconf = '/etc/wpa_supplicant/wpa_supplicant.conf'
	__iwlistbin = which('iwlist')
	__ifconfbin = which('ifconfig')
	__wpapasbin = which('wpa_passphrase')
	__wpasupbin = which('wpa_supplicant')
	stdx = sucommand.stdx
	call = sucommand.call
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg) and type(getattr(self, arg)) is bool:
				setattr(self, arg, True)
		if self._dbg:
			print(WLANConfig.__mro__)
			print('\n'.join(['%s = %s'%((key, val))\
			  for (key, val) in self.__dict__.items()]))
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # prs <bool>
	def prs(self):
		return self._prs
	@prs.setter
	def prs(self, val):
		self._prs = val if type(val) is bool else self._prs
	@property               # iface <str>
	def iface(self):
		return self._iface
	@iface.setter
	def iface(self, val):
		self._iface = val if type(val) is str else self._iface
	@property               # wpaconf <str>
	def wpaconf(self):
		return self._wpaconf
	@wpaconf.setter
	def wpaconf(self, val):
		self._wpaconf = val if type(val) is str else self._wpaconf

	def __dump(self, force=None):
		self.su_ = True
		dumpfile = '/tmp/iwlist.dump'
		if not isup(self.iface) and not ifconfup(self.iface):
			raise RuntimeError('could not bring up iface %s'%(self.iface))
		if not os.path.isfile(dumpfile) or fileage(dumpfile) >= 60:
			data = self.stdx('%s %s scan'%(self.__iwlistbin, self.iface))
			with open(dumpfile, 'w+') as f:
				f.write(data)
		with open(dumpfile, 'r') as f:
			dump = f.read()
		ifconfdown(self.iface)
		return dump

	def inreach(self, essid=None):
		def __blockinfo(block):
			wlblk = {}
			for line in block.split('\n'):
				line = line.strip()
				if line.startswith('Channel'):
					wlblk['channel'] = line.split(':')[1]
				if line.startswith('ESSID'):
					wlblk['ssid'] = line.split(':')[1]
				if line.startswith('Authentication'):
					wlblk['key_mgmt'] = line.split(':')[1]
				if line.startswith('Group'):
					wlblk['group'] = line.split(':')[1]
				if line.startswith('Pairwise'):
					wlblk['pairwise'] = line.split(':')[1]
			if wlblk != {}:
				return wlblk
		wlans = []
		dumpdat = self.__dump()
		if not dumpdat:
			raise RuntimeError('no WLAN in reach')
		for block in dumpdat.split('Cell'):
			if essid:
				if essid in block:
					if __blockinfo(block):
						wlans.append(__blockinfo(block))
				else:
					continue
			if __blockinfo(block):
				wlans.append(__blockinfo(block))
		if wlans != []:
			return wlans

	def readwpa(self):
		if not os.path.isfile(self.wpaconf):
			return False
		essids = []
		with open(self.wpaconf, 'r') as f:
			wpadat = f.readlines()
		for line in wpadat:
			line = line.strip()
			if line.startswith('ssid'):
				essid = line.split('=')[1]
				if essid.startswith('"'):
					essid = essid[1:]
				if essid.endswith('"'):
					essid = essid[:-1]
				essids.append(essid)
		if essids != []:
			return essids

	def writewpa(self, cfgset):
		self.su_= True
		wpadat = ''
		if os.path.isfile(self.wpaconf):
			with open(self.wpaconf, 'r') as f:
				wpadat = f.read()
		with open('/tmp/wpatemp', 'w+') as t:
			t.write(wpadat+'\n'+cfgset)
		if int(self.call(which('mv')+' -f /tmp/wpatemp '+self.wpaconf)) != 0:
			self.call(which('chown'), 'root.root', self.wpaconf)
			return True

	def confgen(self):
		essid = input('Enter name of access point (ESSID)\n')
		pwd = input('enter password for %s\n'%(essid))
		cfgset = '\n'.join([line for line in\
		  self.stdx('%s %s %s'%(self.__wpapasbin, essid, pwd)).split('\n')\
		  if not line.startswith('\t#')])
		if cfgset:
			cfgset = '%s\n\tscan_ssid=1\n\tkey_mgmt=WPA-PSK\n\tproto=RSN\n}\n'\
			  %(cfgset[:-3])
		return cfgset

	def connect(self, essid=None, passwd=None):
		if self.dbg:
			print(bgre(self.connect))
		# first check if the interface already is up
		if isup(self.iface):
			return
		if not isconfd(self.iface):
			self.write_netconf(self.iface, config='wpa')
		# try bringing up any known wlan to avoid access-point-scanning even if
		# an in-reach wlan already is configured and might just be connected
		if ifup(self.iface, dhcp='True'):
			return self.iface
		wlans = self.inreach()
		knows = self.readwpa()
		wpaconfd = [wlan for wlan in wlans for essid in knows\
		  if 'ssid' in wlan.keys() and essid == wlan['ssid'].strip('"')]
		if not wpaconfd:
			self.writewpa(self.confgen())
		if not wlans:
			raise RuntimeError('no WLAN in reach')
		# try to bring up interface 2nd time
		if ifup(self.iface, dhcp='True'):
			return self.ifaces

	def disconnect(self):
		if not isup(self.iface) and not isconfd(self.iface):
			return
		if ifdown(self.iface):
			self.call('killall %s'%(self.__wpasupbin))
			return True














if __name__ == '__main__':
	"""debugging area for modules"""
	#adding ~/bin/modules to sys.path which is usually done by __init__.py
	mdldir = '%s/modules'%(os.path.abspath(__file__).split('/modules')[0])
	if not mdldir in sys.path: 
		sys.path.insert(1, mdldir) 
	del mdldir
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
	wlan = WLANConfig('dbg')
	#print('disconnecting...')
	#print(wlan.disconnect())
	#print('disconnected')
	print('connecting...')
	print(wlan.connect())
	print('connected')
