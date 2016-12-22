# -*- encoding: utf-8 -*-
"""wake on lan python module"""
from socket import \
    socket as _socket, \
    AF_INET as _AF_INET,\
    SOCK_DGRAM as _SOCK_DGRAM, \
    SOL_SOCKET as _SOL_SOCKET, \
    SO_BROADCAST as _SO_BROADCAST

from struct import \
    pack as _pack


def _magicpacket(macaddress):
    """packet from macaddress creating function"""
    """
    Create a magic packet which can be used for wake on lan using the
    mac address given as a parameter.

    Keyword arguments:
    :arg macaddress: the mac address that should be parsed into a magic
                     packet.

    """
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream
    data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += _pack(b'B', int(data[i: i + 2], 16))
    return send_data



def wol(mac, port=9, bcast='255.255.255.255'):
    """magic packet sending function - requires a mac-address"""
    packet = _magicpacket(mac)
    sock = _socket(_AF_INET, _SOCK_DGRAM)
    sock.setsockopt(_SOL_SOCKET, _SO_BROADCAST, 1)
    sock.connect((bcast, int(port)))
    try:
        return sock.send(packet)
    except ValueError as err:
        print(err, file=sys.stderr)
    finally:
        sock.close()






if __name__ == '__main__':
    exit(1)
