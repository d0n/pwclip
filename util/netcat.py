#!/usr/bin/env python3

from socket import \
    socket as sock, \
    timeout as TimeOutError, \
    SOCK_DGRAM, SHUT_WR, \
    AF_INET, SOCK_STREAM

def netcat(host, port, content='telnet', proto='tcp', timeout=5):
	socket = sock(AF_INET, SOCK_STREAM)
	if proto == 'udp':
		socket = sock(AF_INET, SOCK_DGRAM)
	socket.settimeout(timeout)
	try:
		socket.connect((host, int(port)))
	except (ConnectionRefusedError, TimeOutError) as err:
		raise ConnectionError('connection to %s on %s failed by error %s'%(
            host, port, err.errno))
		return 0 if not err.errno else int(err.errno)
	socket.sendall(content.encode())
	socket.shutdown(SHUT_WR)
	data = []
	while True:
		dat = socket.recv(1024)
		if not dat:
			break
		data.append(dat.decode().strip())
	try:
		return data[0] if data else True
	finally:
		socket.close()

