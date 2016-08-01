#!/usr/bin/env python3

import sys
import pwclip
wait = 3
if len(sys.argv) > 1:
	wait = int(sys.argv[1])
pwclip.pwclipper(wait)
