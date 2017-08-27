#!/usr/bin/env python3
from socket import getfqdn

from netaddr import IPNetwork, IPAddress

from net.isip import isip

def addrmask(address, netmask):
	ip = IPNetwork(str(address)+'/'+str(netmask))
	return str(ip.network), str(ip.prefixlen)

def netips(network):
	ips = []
	for ip in IPNetwork(network):
		ips.append(str(ip))
	if ips != []:
		return ips

def iternet(netaddr, mode=None, verbose=None):
	for ip in netips(netaddr):
		host = getfqdn(ip)
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


if __name__ == '__main__':
	exit(1)
