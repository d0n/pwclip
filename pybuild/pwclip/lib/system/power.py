#!/usr/bin/env python3
"""system power management tool"""

# global imports
import os
import sys
from time import sleep

# local relative imports
from colortext import bgre, tabd
from executor import Command
from system import which
from system.uefi import UEFITool

class SystemPower(UEFITool):
	sh_ = True
	su_ = True
	dbg = False
	vrb = False
	_efi = ''
	_power = 'status'
	def __init__(self, *args):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		if self.dbg:
			print(bgre(SystemPower.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property
	def power(self):
		return self._power
	@power.setter
	def power(self, command):
		if not command:
			command = self._power
		if command == 'status':
			self.power = self._status()
		elif command == 'reboot':
			self.reboot()
		elif command == 'shutdown':
			self.shutdown()
		elif command == 'suspend':
			self.suspend()
		else:
			raise AttributeError('unknown command %s'%(command))

	@property               # efi <str>
	def efi(self):
		return self._efi
	@efi.setter
	def efi(self, pattern):
		efihex = self._efihex(pattern)
		if efihex:
			if self.vrb:
				label = self._efilabel(efihex)
			self.nextboot(efihex)
			self._efi = efihex

	def reboot(self):
		if self.dbg:
			print(bgre(self.reboot))
		self.run(which('reboot'))

	def shutdown(self):
		if self.dbg:
			print(bgre(self.shutdown))
		self.run(which('poweroff'))

	def suspend(self):
		if self.dbg:
			print(bgre(self.suspend))
		self.su_ = False
		self.run(
            which('dbus-send'), '--print-reply', '--system', \
            '--dest="org.freedesktop.login1"', '/org/freedesktop/login1', \
            'org.freedesktop.login1.Manager.Suspend', 'boolean:true'
            )











if __name__ == '__main__':
	# module debigging area
	print('\n'.join(m for m in dir()))
