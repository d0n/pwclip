#!/usr/bin/env python3

from socket import \
    socket as _socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout as _timeout

from colortext import error

def netcat(host, port, content='telnet', proto='tcp', timeout=5):
	sock = _socket(AF_INET, SOCK_STREAM)
	if proto == 'udp':
		sock = _socket(AF_INET, SOCK_DGRAM)
	sock.settimeout(timeout)
	try:
		sock.connect((host, int(port)))
	except (ConnectionRefusedError, _timeout) as err:
		error('connecting ', host, ' on ', '%s '%port, err)
		return 0 if not err.errno else int(err.errno)
	sock.sendall(content.encode())
	sock.shutdown(SHUT_WR)
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

