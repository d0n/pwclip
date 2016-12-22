#!/usr/bin/env python3
# global imports
import os
import sys
# local relative imports
# default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))
__version__ = '0.1'


class WWANConfig(object):
	pass










if __name__ == '__main__':
	# module debugging area
	print('\n'.join(m for m in dir()))
