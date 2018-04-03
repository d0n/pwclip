#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""ip checker using re.search regular expression"""

from re import search

def isip(pattern):
	"""return true if input is possibly an ip-address"""
	# return True if "pattern" is RFC conform IP otherwise False
	iplike = r'^(?!0+\.0+\.0+\.0+|255\.255\.255\.255)' \
        r'(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)' \
        r'\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
	if search(iplike, pattern):
		return True
	return False

