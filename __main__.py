#!/usr/bin/env python3
import sys
import pwclip
pwclip.pwclipper(int(3 if len(sys.argv) != 2 else sys.argv[1]))
