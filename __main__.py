#!/usr/bin/env python3
import sys
import pwclip
pwclip.pwclipper(3 if not len(sys.argv) == 2 else sys.argv[1])
