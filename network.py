#!/usr/bin/env python3
"""common network function definitions"""
# global imports
import re
import os
import sys
import socket
import struct
import netifaces
from fcntl import ioctl
from time import sleep
from netaddr import IPNetwork, IPAddress
from colortext import error

__version__ = '1.2'
netdir = '/sys/class/net'

def addrmask(address, netmask):
	ip = IPNetwork(str(address)+'/'+str(netmask))
	return str(ip.network), str(ip.prefixlen)

def netips(network):
	ips = []
	for ip in IPNetwork(network):
		ips.append(str(ip))
	if ips != []:
		return ips

def ifaces(netdir=netdir):
	devs = []
	for dev in os.listdir(netdir):
		dev = dev.strip()
		devs.append(dev)
	return devs

def mac(iface, byte=False):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = ioctl(
        sock.fileno(), 0x8927,
        struct.pack('256s', bytes(iface[:15], 'utf-8')))
	if byte:
		smac = ''.join(['%02x'%c for c in info[18:24]])
		mac = b''
		for i in range(0, 12, 2):
			m = int(smac[i:i+2], 16)
			mac += struct.pack('!B', m)
	else:
		mac = ':'.join(['%02x'%c for c in info[18:24]])
	return mac

def macs(byte=False):
	return [mac(i, byte) for i in ifaces()]

def ifaddrs(iface, ipv4=True, ipv6=True):
	ip4s = []
	ip6s = []
	if ipv4:
		try:
			for ip4 in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
				ip4s.append(ip4)
		except KeyError:
			pass
	if ipv6:
		try:
			for ip6 in netifaces.ifaddresses(iface)[netifaces.AF_INET6]:
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


def isip(pattern):
	# return True if "pattern" is RFC conform IP otherwise False
	iplike = '^(?!0+\.0+\.0+\.0+|255\.255\.255\.255)' \
	    '(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)' \
	    '\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
	if re.search(iplike, pattern):
		return True
	return False

def fqdn(name):
	fqdn = socket.getfqdn(name) if name else os.uname()[1]
	if fqdn:
		return fqdn
	return name

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


def haslink(iface):
	linkfile = netdir+'/'+iface+'/carrier'
	if os.path.isfile(linkfile):
		try:
			with open(linkfile, 'r') as f:
				link = f.read()
			if link.strip() == '1':
				return True
		except OSError:
			return False


def isup(iface):
	statefile = netdir+'/'+iface+'/operstate'
	state = None
	if os.path.isfile(statefile):
		try:
			with open(statefile, 'r') as f:
				state = f.read()
		except:
			state = False
		finally:
			if state:
				if state.strip() == 'up':
					return True



def gateway(network=None, ipv4=True, ipv6=False):
	nets = []
	if network:
		ip = IPNetwork(network)
		nets.append(ip.network)
	else:
		for iface in ifaces():
			if iface == 'lo':
				continue
			addrs = ifaddrs(iface, ipv4=ipv4, ipv6=ipv6)
			if not addrs:
				continue
			for ipv in addrs:
				net = '%s/%s' %(addrs[ipv]['addr'], addrs[ipv]['netmask'])
				ip = IPNetwork(net)
				if ip.network:
					nets.append(str(ip.network))
	gates = []
	for net in nets:
		net, last = str(net).split('.')[:-1], str(net).split('.')[-1]
		last = int(last)+1
		if not network or not '/' in network:
			last = 1
		net.append(last)
		gates.append('.'.join(str(n) for n in net))
	return gates


def askdns(host):
	try:
		dnsinfo = socket.gethostbyaddr(host)
	except (socket.gaierror, socket.herror, TypeError) as e:
		return
	if isip(host):
		return dnsinfo[0]
	if len(dnsinfo[2]) == 1:
		return dnsinfo[2][0]
	return dnsinfo[2]

def vpninfo():
	for iface in interfaces():
		ifac = re.sub(r'\d$', '', iface)
		if ifac == 'tun':
			return ifaddresses(iface)[IP4]


def iftype(iface, netdir=netdir):
	infofile = '%s/%s/uevent'%(netdir, iface)
	if os.path.isfile(infofile):
		with open(infofile, 'r') as f:
			ifinfo = f.readlines()
		for line in ifinfo.split('\n'):
			if 'DEVTYPE' in line:
				return str(line.split('=')[1]).strip()
			elif 'INTERFACE' in line:
				return str(line.split('=')[1][:-1]).strip()
	return re.sub(r'\d$', '', iface)


def netcat(host, port, content='telnet', proto='tcp', timeout=5):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if proto == 'udp':
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(timeout)
	try:
		sock.connect((host, int(port)))
	except ConnectionRefusedError as err:
		error('connecting', host, 'on', port, err)
		return int(err.errno)
	sock.sendall(content.encode())
	sock.shutdown(socket.SHUT_WR)
	data = []
	while True:
		dat = sock.recv(1024)
		if not dat:
			break
		data.append(dat.decode().strip())
	try:
		return data[0] if data else True
	finally:
		sock.close()


def raflookup(host):
	if host:
		lookup = askdns(host)
		if lookup:
			reverse = askdns(lookup)
			return lookup, reverse

def iternet(netaddr, mode=None, verbose=None):
	for ip in netips(netaddr):
		host = socket.getfqdn(ip)
		if mode == 'both':
			ipdns = ip, None
			if host != ip:
				ipdns = ip, host
		elif mode == 'block':
			if host != ip:
				ipdns = ip, host
			else:
				continue
		elif mode == 'avail':
			if host == ip:
				ipdns = ip, None
			else:
				continue
		yield ipdns

def currentnets():
	for iface in anyifconfd():
		ifips = ifaddrs(iface)
		if ifips and 'ipv4' in ifips.keys():
			for ips in ifips['ipv4']:
				if 'addr' in ips:
					netaddress, netbits = addrmask(
						ips['addr'], ips['netmask'])
					yield '%s/%s'%(netaddress, netbits)














if __name__ == '__main__':
	# print known functions
	print('\n'.join(d for d in dir()))
#	print(interfaces().keys())
#	import yaml
#	with open
#	vpncfg = yaml.load(f)[os.uname()[1]]['vpn']
#	vpncfg = {'cert': 'blap_lpelzer.crt', 'user': 'lpelzer', 'dir': '~/.vpn',\
#  'gate': 'gw-ma-vpn.bs.kae.de.oneandone.net', 'key': 'blap_lpelzer.key',\
#  'office': 'office-ca.crt', 'pidfile': 'openconnect.pid',\
#  'dns': '172.19.254.1, 172.19.255.1'}
#	wlancfg = {'iface':'wlan0',\
#  'wpaconf':'/etc/wpa_supplicant/wpa_supplicant.conf'}
#	ethcfg = {'iface':'eth0'}
#	eth = ETHConfig()
#	print(ifdown('eth0'))
#	print(askdns(sys.argv[1]))
	#print(isip('266.2.2.2'))
#!/usr/bin/python
import sys, socket

if __name__ == '__main__':
	netcat(sys.argv[1], sys.argv[2], sys.argv[4], proto=sys.argv[3])
