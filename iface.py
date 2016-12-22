#!/usr/bin/env python3

from re import sub

from os import listdir

from os.path import isfile

from netifaces import ifaddresses, AF_INET

from net.addr import addrmask

def ifaces(netdir='/sys/class/net'):
	return [d.strip() for d in listdir(netdir)]

def ifaddrs(iface, ipv4=True, ipv6=True):
	ip4s = []
	ip6s = []
	if ipv4:
		try:
			for ip4 in ifaddresses(iface)[AF_INET]:
				ip4s.append(ip4)
		except KeyError:
			pass
	if ipv6:
		try:
			for ip6 in ifaddresses(iface)[AF_INET6]:
				if 'addr' in ip6.keys() and '%' in ip6['addr']:
					ip6['addr'] = ip6['addr'].split('%')[0]
				ip6s.append(ip6)
		except KeyError:
			pass
	if ip4s and ip6s:
		return {'ipv4':ip4s, 'ipv6':ip6s}
	elif ip4s:
		return {'ipv4':ip4s}
	elif ip6s:
		return {'ipv6':ip6s}

def anyifconfd():
	confdifs = []
	for iface in ifaces():
		if iface == 'lo':
			continue
		ipaddrs = ifaddrs(iface)
		if ipaddrs:
			for ipv in ipaddrs:
				for ips in ipaddrs[ipv]:
					if 'addr' in ips.keys() and not iface in confdifs:
						confdifs.append(iface)
						break
	return confdifs

def isconfd(iface):
	if iface in anyifconfd():
		return True

def haslink(iface, netdir='/sys/class/net'):
	linkfile = netdir+'/'+iface+'/carrier'
	if isfile(linkfile):
		try:
			with open(linkfile, 'r') as f:
				link = f.read()
			if link.strip() == '1':
				return True
		except OSError:
			return False

def isup(iface, netdir='/sys/class/net'):
	statefile = netdir+'/'+iface+'/operstate'
	state = None
	if isfile(statefile):
		try:
			with open(statefile, 'r') as f:
				state = f.read()
		except:
			state = False
		finally:
			if state:
				if state.strip() == 'up':
					return True


def iftype(iface, netdir='/sys/class/net'):
	infofile = '%s/%s/uevent'%(netdir, iface)
	if isfile(infofile):
		with open(infofile, 'r') as f:
			ifinfo = f.readlines()
		for line in ifinfo.split('\n'):
			if 'DEVTYPE' in line:
				return str(line.split('=')[1]).strip()
			elif 'INTERFACE' in line:
				return str(line.split('=')[1][:-1]).strip()
	return re.sub(r'\d$', '', iface)

def currentnets():
	for iface in anyifconfd():
		ifips = ifaddrs(iface)
		if ifips and 'ipv4' in ifips.keys():
			for ips in ifips['ipv4']:
				if 'addr' in ips:
					netaddress, netbits = addrmask(
                        ips['addr'], ips['netmask'])
					yield '%s/%s'%(netaddress, netbits)
