# -*- encoding: utf-8 -*-
"""wake on lan python module"""
from sys import stderr

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST

from struct import pack

def _magicpacket(macaddress):
	"""packet from macaddress creating function"""
	if len(macaddress) == 12:
		pass
	elif len(macaddress) == 17:
		sep = macaddress[2]
		macaddress = macaddress.replace(sep, '')
	else:
		raise ValueError('Incorrect MAC address format')
	data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
	send_data = b''
	for i in range(0, len(data), 2):
		send_data += pack(b'B', int(data[i: i + 2], 16))
	return send_data



def wol(mac, port=9, bcast='255.255.255.255'):
	"""magic packet sending function - requires a mac-address"""
	packet = _magicpacket(mac)
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	sock.connect((bcast, int(port)))
	try:
		return sock.send(packet)
	except ValueError as err:
		print(err, file=stderr)
	finally:
		sock.close()






if __name__ == '__main__':
    exit(1)
