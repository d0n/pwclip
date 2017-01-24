from socket import socket, AF_INET, SOCK_DGRAM

from struct import pack

from net.iface import ifaces

def mac(iface, byte=False):
	sock = socket(AF_INET, SOCK_DGRAM)
	info = ioctl(
		sock.fileno(), 0x8927,
		pack('256s', bytes(iface[:15], 'utf-8')))
	if byte:
		smac = ''.join(['%02x'%c for c in info[18:24]])
		mac = b''
		for i in range(0, 12, 2):
			m = int(smac[i:i+2], 16)
			mac += pack('!B', m)
	else:
		mac = ':'.join(['%02x'%c for c in info[18:24]])
	return mac

def macs(byte=False):
	return [mac(i, byte) for i in ifaces()]
