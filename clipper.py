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
pwclip - password to clipboard (mouse coupy/paste buffer) manager
"""
from sys import argv

from os import environ, fork

from time import sleep

try:
	from tkinter import StringVar, Button, Entry, Frame, Label, Tk
except ImportError:
	from Tkinter import StringVar, Button, Entry, Frame, Label, Tk

from system import clips, inputgui

from cypher import ykchalres, passcrypt

def clipper(wait=3, mode='yk'):
	"""gui representing function"""
	copy, paste = clips()
	oclp = paste()
	if mode == 'yk':
		copy(ykchalres(inputgui()))
	elif mode == 'pc':
		copy(passcrypt(inputgui()))
	if oclp != paste():
		try:
			sleep(int(wait))
		finally:
			copy(oclp)
