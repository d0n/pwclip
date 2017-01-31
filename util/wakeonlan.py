# -*- encoding: utf-8 -*-
"""wake on lan python module"""
from sys import stderr

from socket import \
    AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, socket as sock

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
	socket = sock(AF_INET, SOCK_DGRAM)
	socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	socket.connect((bcast, int(port)))
	try:
		return socket.send(packet)
	except ValueError as err:
		print(err, file=stderr)
	finally:
		socket.close()






if __name__ == '__main__':
    exit(1)
