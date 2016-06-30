#!/usr/bin/env python3
"""
d0nkey - yubikey module
"""
import sys
from yubico import \
    find_yubikey, yubikey, \
    yubico_exception

from binascii import hexlify

def _yubikeys(dbg=False, ykser=None):
	"""
	return a list of yubikeys objects
	"""
	keys = []
	for i in range(0, 255):
		try:
			key = find_yubikey(debug=dbg, skip=i)
		except yubikey.YubiKeyError:
			break
		if ykser and int(ykser) != int(key.serial()):
			continue
		yield key

def _slotchalres(yk, chal, slot):
	try:
		return hexlify(yk.challenge_response(
			chal.ljust(64, '\0').encode(), slot=slot)).decode()
	except yubico_exception.YubicoError as err:
		pass

def _chalres(chal, slot=None, ykser=None):
	if not slot:
		return [_slotchalres(k, chal, s) for k in _yubikeys(ykser=ykser) for s in (2, 1)]
	res = [_slotchalres(k, chal, slot) for k in _yubikeys(ykser=ykser)]
	return res if len(res) > 1 else res[0]


