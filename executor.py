#!/usr/bin/python3
"""executing (remote) commands module"""
import sys, os
from socket import getfqdn as fqdn
from subprocess import call, Popen, PIPE
# for subprocess version compatibility while DEVNULL is new in subprocess
try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = open('/dev/null')

from misc import which, whoami

class Command(object):
	"""(remote) command execution module"""
	_sh_ = False
	_su_ = False
	_dbg_ = False
	def __init__(self, *args):
		for arg in args:
			arg = '_%s_'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
	# rw properties
	@property               # sh_ <bool>
	def sh_(self):
		return self._sh_
	@sh_.setter
	def sh_(self, val):
		self._sh_ = val #if isinstance(val, bool) else self._sh_

	@property               # su_ <bool>
	def su_(self):
		return self._su_
	@su_.setter
	def su_(self, val):
		self._su_ = val if isinstance(val, bool) else self._su_

	@property                # dbg_ <bool>
	def dbg_(self):
		return self._dbg_
	@dbg_.setter
	def dbg_(self, val):
		self._dbg_ = val if isinstance(val, bool) else self._dbg_

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
	def __sucmd(commands):
		if 'sudo' in commands[0]:
			del commands[0]
		if int(os.getuid()) != 0:
			commands.insert(0, which('sudo'))
		return commands

	def _sudo(self, commands=None):
		"""privilege checking function"""
		if not commands:
			if int(call([which('sudo'), '-v'])) == 0:
				return True
		return self._sucmd(commands)

	def __cmdprep(self, commands):
		commands = self.__list(commands)
		if self.su_:
			commands = self._sudo(commands)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg_:
			print(
                'cmd = `%s`\n\tsh = %s, su = %s'%(commands, self.sh_, self.su_)
            )
		return commands

	def run(self, *commands):
		"""just run the command and return the processes PID"""
		commands = self.__cmdprep(commands)
		return Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, *commands):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		commands = self.__cmdprep(commands)
		return int(call(commands, shell=self.sh_))

	def stdx(self, *commands):
		"""command execution which returns STDERR and/or STDOUT"""
		commands = self.__cmdprep(commands)

		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, *commands):
		"""command execution which returns STDOUT only"""
		commands = self.__cmdprep(commands)
		prc = Popen(commands, stdout=PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate()
		if out:
			return out.decode()

	def stde(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		_, err = prc.communicate()
		if err:
			return err.decode()

	def erno(self, *commands):
		"""command execution which returns the exitcode only"""
		commands = self.__cmdprep(commands)
		prc = Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate()
		return int(prc.returncode)

	def oerc(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		return out.decode(), err.decode(), prc.returncode



if __name__ == '__main__':
	exit(0)
