#!/usr/bin/env python3
"""network parser module"""
# global imports
import re
import os
import sys
import xml.etree.ElementTree as etree

# local relative imports
from lib.colortext import bgre
from lib.misc import which
from lib.executor import Command

# default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))

class NetworkInterfacesParser(object):
	_dbg = None
	_prs = None
	_netconf = '/etc/network/interfaces'
	__tmpfile = '/tmp/network_interfaces'
	sudo = Command('su')
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(NetworkInterfaces.__mro__))
			for (key, val) in self.__dict__.items():
				print(bgre(key, '=', val))
	# rw properties
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
	@property               # netconf <str>
	def netconf(self):
		return self._netconf
	@netconf.setter
	def netconf(self, val):
		self._netconf = val if type(val) is str else self._netconf

	def __read(self):
		with open(self.netconf, 'r') as nif:
			return nif.read()

	def __write(self, netcfg):
		try:
			with open(self.netconf, 'w+') as nif:
				nif.write(netcfg)
		except IOError as err:
			with open(self.__tmpfile, 'w+') as tmp:
				tmp.write(netcfg)
			self.sudo.call(
			    '%s -f %s %s'%(which('cp'), self.__tmpfile, self.netconf))
		return True

	def __ifline(self, iface, mode='dhcp', config=None):
		ifline = 'iface %s inet %s\n'%(iface, mode)
		if mode == 'static':
			if config:
				if type(config) is dict:
					for (key, val) in config.items():
						if key == 'ip':
							key = 'address'
						ifline = '%s\t%s %s\n'%(ifline, key, val)
				else:
					raise TypeError(
					    'cannot handle config type %s type dict expected'%(
					        type(config))
					    )
			else:
				raise RuntimeError(
				    'config is needed when using static configuration mode')
		else:
			if config == 'wpa':
				ifline = '%s\twpa-driver wext,nl80211\n\twpa-conf ' \
				    '/etc/wpa_supplicant/wpa_supplicant.conf\n'%(ifline)
		return ifline

	def read_netconf(self):
		autoifs = self.__read()
		autos = list(a for auto in autoifs.split(
		    '\n') for a in auto.split(
		        ' ') if auto.startswith('auto') if a != 'auto'
		    )
		ifaces = ['iface %s'%(l.strip()) for l in autoifs.split(
		    'iface ') if l.strip() and not l.startswith('auto')]
		return autos, ifaces

	def write_netconf(self, iface, mode='dhcp', auto=None, config=None):
		if self.dbg:
			print(bgre(self.write_netconf))
		if auto in (True, False):
			self.prs = auto
		if mode == 'wpa':
			mode = 'dhcp'
			config = 'wpa'
		elif mode not in ('static', 'dhcp', 'delete'):
			raise RuntimeError('\n%s\nunknown configuration mode, %s'%(
			    self.write_netconf, mode))
		autos, ifconfs = self.read_netconf()
		if mode == 'delete':
			autos = [a for a in autos if a != iface]
			ifconfs = [c for c in ifconfs if iface != c.split(' ')[1]]
		else:
			if self.prs:
				autos = [a for a in autos if a != iface] + [iface]
			elif self.prs is False:
				autos = [a for a in autos if a != iface]
		autoline = 'auto %s\n'%(' '.join(a for a in autos))
		iflines = []
		for ifconf in ifconfs:
			if ifconf.split()[1] == iface:
				if mode == 'delete':
					continue
				ifline = self.__ifline(iface, mode, config)
			else:
				ifline = '%s\n'%(ifconf.strip())
			iflines.append(ifline)
		if (mode != 'delete' and not
		      [l for l in iflines if l.split()[1] == iface]):
			iflines.append(self.__ifline(iface, mode, config))
		#print(autoline+'\n'.join(l for l in iflines))
		if self.__write(
		      '%s\n%s'%(autoline, '\n'.join(l for l in iflines))):
			return True



class WPASupplicantParser(object):
	_dbg = None
	_wpacfg = '/etc/wpa_supplicant/wpa_supplicant.conf'
	__wpapasbin = which('wpa_passphrase')
	cmdx = Command()
	sudo = Command('su')
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
			print(bgre(ETHConfig.__mro__))
			for (key, val) in self.__dict__.items():
				print(bgre(key, '=', val))
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # wpacfg <str>
	def wpacfg(self):
		return self._wpacfg
	@wpacfg.setter
	def wpacfg(self, val):
		self._wpacfg = val if val is str else self._wpacfg

	@staticmethod
	def __password(essid):
		from getpass import getpass
		return getpass('Enter password for %s\n'%(essid))

	def __pskpwhash(self, essid, password):
		return [
		    p.strip().split('=')[1] for p in self.cmdx.stdo(
		        self.__wpapasbin, essid, password
		        ).split('\n') if p and p.strip().startswith('psk')
		    ][0]

	def _confgen(self, essid, passwd=None):
		psk = self.__pskpwhash(essid, passwd or self.__password(essid))
		return {essid:{
		    'psk': psk, 'scan_ssid': '1',
		    'key_mgmt': 'WPA-PSK', 'proto': 'RSN'}
		    }

	def _read(self):
		with open(self.wpacfg, 'r') as wpaf:
			wpanets = [c.strip('{}\n') for c in wpaf.read().split('network=')]
		wpas = {}
		for confs in wpanets:
			cfgs = {}
			ssid = None
			for line in confs.split('\n'):
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				if line.startswith('ssid'):
					ssid = line.split('=')[1].strip('"')
					continue
				cfgs[line.split('=')[0]] = line.split('=')[1]
			wpas[ssid] = cfgs
		return wpas

	def _write(self, essid, passwd=None):
		wpaconf = self._read()
		if essid in wpaconf:
			return wpaconf
		wpaconf[essid] = self._confgen(essid, passwd)
		wpaconfig = ''
		for wpa in wpaconf:
			if not wpa:
				continue
			wpaconfig = '%snetwork={\n\tssid="%s"'%(wpaconfig, wpa)
			for (key, val) in wpaconf[wpa].items():
				wpaconfig = '%s\n\t%s=%s'%(wpaconfig, key, val)
			wpaconfig = '%s\n}\n'%(wpaconfig.strip())
		try:
			with open(self.wpacfg, 'w+') as wpaf:
				wpaf.write(wpaconfig)
		except PermissionError:
			with open('/tmp/wpatemp.conf', 'w+') as wpatmp:
				wpatmp.write(wpaconfig)
			try:
				self.sudo.call(which('cp'), '/tmp/wpatemp.conf', self._wpacfg)
			finally:
				self.cmdx.call(which('rm'), '/tmp/wpatemp.conf')



class DhclientParser(object):
	host = os.uname()[1]
	def __init__(self, config):
		self.conf = config

	def check(self, optarg=None):
		if optarg:
			if optarg in self.data:
				return self.data
		return self.data

	def readdhcp(self):
		try:
			with open(self.conf, 'r') as f:
				self.data = f.read()
		except OSError as e:
			error(e)
		data = ''
		for line in str(self.data).split('\n'):
			if not line or line.startswith('#'):
				continue
			data = data+line
		# get varialbe:value pairs from line of dhclient.conf
		def __dhcvars(line):
			for line in line.split('\\t'):
				# skip empty lines
				line = line.strip()
				if not line:
					continue
				if '=' in line:
					var = line.split('=')[0]
					val = line.split('=')[1]
				elif ',' in line:
					if not str(line.split(' ')[0]).endswith(','):
						var = line.split(' ')[0]
						line = line[len(var):]
					try:
						val
					except UnboundLocalError:
						val = ''
					for va in line.split('\n'):
						val = val+va.strip()+' '
				elif '"' in line:
					var = line.split('"')[0]
					val = line.split('"')[-2]
				else:
					var = ''
					for v in line.split(' ')[:-1]:
						var = var+v+' '
					val = line.split(' ')[-1]
				var = str(var).strip()
				val = str(val).strip()
				if var and val:
					return {var:val}
		config = []
		for line in data.split(';'):
			# skip empty lines
			line = line.strip()
			if not line:
				continue
			# begin or end indented block on indicator "{" and "}"
			if '{' in line or '}' in line:
				if '{' in line and '}' in line:
					config.append({blockname:block})
					block = []
					blockname = str(re.sub(r'\}', '', str(line.split(' ')[0]).strip())).strip()
				elif '{' in line:
					block = []
					blockname = str(re.sub(r'\}', '', str(line.split(' ')[0]).strip())).strip()
				elif '}' in line:
					config.append({blockname:block})
				line = '\t'+str(re.sub(r'(\{|\n|\t|\}|'+str(blockname)+')', '', str(line))).strip()
			try:
				if __dhcvars(line):
					block.append(__dhcvars(line))
			except UnboundLocalError:
				if __dhcvars(line):
					config.append(__dhcvars(line))
		return config

	def writedhcp(self, settings):
		def __check_plaus(conf):
			iface = None
			hostname = os.uname()[1]
			netdir = '/sys/class/net'
			for iface in conf:
				if iface in os.listdir(netdir):
					return True
		if not __check_plaus(settings):
			raise RuntimeError('parser plausability check failed')
		config = self.read()
		#print(config)
		for section in config:
			for var_val in section:
				subsec = None
				if type(section[var_val]) is list:
					for subsec in section[var_val]:
						print('\t', subsec)
			if subsec:
				continue
			print(section)
		"""
		for iface in settings:
			for set_val in settings[iface]:
				for cfg_val in config:
					for cfg in cfg_val:
						if set_val in cfg:
							print(set_val, cfg) #, settings[set_val])
		print('\n\n')
		print(settings)
		"""








if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	wpa = WPASupplicantParser()
	print(wpa._write('FlyingLAN'))
