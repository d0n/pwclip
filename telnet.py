
from socket import \
    socket as _socket, \
    SHUT_WR as _SHUT_WR, \
    AF_INET as _AF_INET, \
    SOCK_DGRAM as _SOCK_DGRAM, \
    SOCK_STREAM as _SOCK_STREAM


def telnet(host, port, proto='tcp', timeout=5):
    sock = _socket(_AF_INET, _SOCK_STREAM)
    if proto == 'udp':
        sock = _socket(_AF_INET, _SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, int(port)))
        sock.shutdown(_SHUT_WR)
    except ConnectionRefusedError as err:
        return False
    finally:
        sock.close()
    return True
