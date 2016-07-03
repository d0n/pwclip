#!/usr/bin/env python3
"""
d0nkey - yubikey module
"""
import sys
from os import environ
from yubico import \
    find_yubikey, yubikey, \
    yubico_exception

from yubico.yubikey_usb_hid import YubiKeyHIDDevice

from yubico.yubikey_neo_usb_hid import YubiKeyNEO_USBHID

from yubico.yubikey_4_usb_hid import YubiKey4_USBHID

from binascii import hexlify

from pyperclip import copy as copyclip

def _yubikeys(ykser=None, dbg=None):
	"""
	return a list of yubikeys objects
	"""
	keys = {}
	for i in range(0, 255):
		try:
			key = find_yubikey(debug=dbg, skip=i)
		except yubikey.YubiKeyError:
			break
		if ykser and int(ykser) != int(key.serial()):
			continue
		keys[key.serial()] = key
	return keys

def _slotchalres(yk, chal, slot):
	try:
		return hexlify(yk.challenge_response(
            chal.ljust(64, '\0').encode(), slot=slot)).decode()
	except yubico_exception.YubicoError as err:
		pass

def chalres(chal, slot=2, ykser=None):
	keys = _yubikeys(ykser)
	for (ser, key) in keys.items():
		return _slotchalres(key, chal, slot)
	"""
	if not slot:
		return [_slotchalres(k, chal, s) for k in _yubikeys(ykser=ykser) for s in (2, 1)]
	res = [_slotchalres(k, chal, slot) for k in _yubikeys(ykser=ykser)]
	return res if len(res) > 1 else res[0]
	"""

def cpchalres(chal=None, slot=2, ykser=None):
	if not ykser:
		ykser = '' if 'YKSERIAL' not in environ.keys() else environ['YKSERIAL']
	if not chal:
		chal = input('enter challenge: ')
	__res = chalres(chal, slot, ykser)
	copyclip(__res)
