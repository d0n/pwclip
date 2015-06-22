#!/usr/bin/env python3
"""system power management tool"""

# global imports
import os
import sys
from time import sleep

# local relative imports
sys.path = [os.path.expanduser('~/bin')] + [
    p for p in sys.path if p != os.path.expanduser('~/bin')]
from modules.wrapper.uefi import UEFITool
from modules.system.executor import Command
from modules.system.common import which

# default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))
__version__ = '0.2'

class SystemPower(UEFITool):
	_sh_ = True
	_su_ = True
	_dbg = False
	_vrb = False
	_efi = ''
	_power = 'status'
	def __init__(self, *args):
		for arg in args:
			arg = '_%s' %(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val
	@property
	def power(self):
		return self._power
	@power.setter
	def power(self, command):
		if not command:
			command = self._power
		if command == 'status':
			self._power = self._status()
		elif command == 'reboot':
			self._reboot()
		elif command == 'shutdown':
			self._shutdown()
		elif command == 'suspend':
			self._suspend()
		else:
			raise AttributeError('unknown command %s'%(command))
	@property               # efi <str>
	def efi(self):
		return self._efi
	@efi.setter
	def efi(self, pattern):
		efihex = self._efihex(pattern)
		if efihex:
			if self._vrb:
				label = self._efilabel(efihex)
			self.nextboot(efihex)
			self._efi = efihex

	def _reboot(self):
		self.run(which('reboot'))

	def _shutdown(self):
		self.run(which('shutdown'), '-P', 'now')

	def _suspend(self):
		self.su_ = False
		self.run(
		    which('dbus-send'), '--print-reply', '--system', \
		    '--dest="org.freedesktop.login1"', '/org/freedesktop/login1', \
		    'org.freedesktop.login1.Manager.Suspend', 'boolean:true'
		    )











if __name__ == '__main__':
	# module debigging area
	print('\n'.join(m for m in dir()))
