#!/usr/bin/python3
"""executing (remote) commands module"""
import os

from socket import getfqdn as fqdn
from subprocess import call, Popen, PIPE

from lib import which, whoami

# for subprocess version compatibility while DEVNULL is new in subprocess
try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = open('/dev/null')

class Command(object):
	"""(remote) command execution module"""
	_sh_ = False
	_su_ = False
	_dbg = False
	_user_ = whoami()
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg[1:], True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key[1:], val)
		if self.dbg:
			print(Command.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
	# rw properties
	@property               # sh_ <bool>
	def sh_(self):
		return self._sh_
	@sh_.setter
	def sh_(self, val):
		self._sh_ = val if isinstance(val, bool) else self._sh_
	@property               # su_ <bool>
	def su_(self):
		return self._su_
	@su_.setter
	def su_(self, val):
		self._su_ = val if isinstance(val, bool) else self._su_
	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val
	@property                # user_ <str>
	def user_(self):
		return self._user_
	@user_.setter
	def user_(self, val):
		self._user_ = val if type(val) is str else self._user_

	@staticmethod
	def __list(*commands):
		"""commands to list converter"""
		cmds = []
		try:
			cmds = eval(commands)
		except (SystemError, TypeError):
			#print(commands)
			for cmmd in commands:
				if isinstance(cmmd, str):
					if ' ' in cmmd:
						for cmd in cmmd.split(' '):
							cmds.append(cmd)
					else:
						cmds.append(cmmd)
				else:
					for cmd in cmmd:
						cmds.append(cmd)
		return list(cmds)

	@staticmethod
	def __str(*commands):
		"""commands to str converter"""
		return ' '.join(str(command) for command in list(commands))

	@staticmethod
	def _sudo():
		"""privilege checking function"""
		if int(os.getuid()) != 0:
			if int(call([which('sudo'), '-v'])) == 0:
				return True

	def _sudocmd(self, *commands):
		"""sudo to cmd prepending function"""
		if 'sudo' in commands[0]:
			del commands[0]
		if self._sudo():
			commands.insert(0, which('sudo'))
		return commands

	def run(self, *commands):
		"""just run the command and return the processes PID"""
		commands = self.__list(*commands)
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		return Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, *commands):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		return int(call(commands, shell=self.sh_))

	def stdx(self, *commands):
		"""command execution which returns STDERR and/or STDOUT"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, *commands):
		"""command execution which returns STDOUT only"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		prc = Popen(commands, stdout=PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate()
		if out:
			return out.decode()

	def stde(self, *commands):
		"""command execution which returns STDERR only"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		_, err = prc.communicate()
		if err:
			return err.decode()

	def erno(self, *commands):
		"""command execution which returns the exitcode only"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		prc = Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate()
		return int(prc.returncode)

	def oerc(self, *commands):
		"""command execution which returns STDERR only"""
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_, 'su =', self.su_)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		return out.decode(), err.decode(), prc.returncode



if __name__ == '__main__':
	exit(0)
