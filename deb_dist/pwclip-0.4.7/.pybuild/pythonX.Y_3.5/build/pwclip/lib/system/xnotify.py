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
"""linux x-notification library"""
from inspect import stack
try:
	import gi
	gi.require_version('Notify', '0.7')
	from gi.repository import Notify as xnote
except AttributeError:
	def xnotify(*args): return 

def xnotify(msg, name=stack()[1][3], wait=3):
	xnote.init(str(name))
	note = xnote.Notification.new(msg)
	wait = int(wait)*600
	note.set_timeout(wait)
	note.show()
