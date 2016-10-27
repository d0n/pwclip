#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""
yubikey challenge-response lib
"""

from os import environ

from binascii import hexlify

from yubico import \
    find_yubikey, yubikey, \
    yubico_exception

def yubikeys(ykser=None, dbg=None):
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

def ykslotchalres(yk, chal, slot):
	"""
	challenge-response function using with given
	challenge (chal) for slot on yubikey found by yubikeys()
	"""
	try:
		return hexlify(yk.challenge_response(
			chal.ljust(64, '\0').encode(), slot=slot)).decode()
	except yubico_exception.YubicoError:
		pass

def ykchalres(chal, slot=2, ykser=None):
	"""
	challenge-response function using specified slot
	or default (2) as wrapping function for yubikeys() and slotchalres()
	"""
	if 'YKSERIAL' in environ.keys():
		ykser = ykser if ykser else environ['YKSERIAL']
	keys = yubikeys(ykser)
	for (_, key) in keys.items():
		res = ykslotchalres(key, chal, slot)
		if res:
			return res

