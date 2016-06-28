#!/usr/bin/env python3
"""
yubikey module
"""

import sys
import yubico

def yubikeys(debug):
	"""
	return a list of yubikeys available
	"""
	keys = []
	try:
		skip = 0
		while skip < 255:
			yk = yubico.find_yubikey(debug=debug, skip=skip)
			keys.append(yk)
			skip += 1
	except yubico.yubikey.YubiKeyError:
		pass
	return keys
