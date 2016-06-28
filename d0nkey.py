#!/usr/bin/env python3
"""
yubikey module
"""

import sys
import yubico

def yubikeys(dbg=False):
	"""
	return a list of yubikeys available
	"""
	keys = []
	try:
		skip = 0
		while skip < 255:
			yk = yubico.find_yubikey(debug=dbg, skip=skip)
			keys.append(yk)
			skip += 1
	except yubico.yubikey.YubiKeyError:
		pass
	return keys
