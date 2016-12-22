#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM

def netcat(host, port, content='telnet', proto='tcp', timeout=5):
	sock = socket(AF_INET, SOCK_STREAM)
	if proto == 'udp':
		sock = socket(AF_INET, SOCK_DGRAM)
	sock.settimeout(timeout)
	try:
		sock.connect((host, int(port)))
	except ConnectionRefusedError as err:
		error('connecting', host, 'on', port, err)
		return int(err.errno)
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

