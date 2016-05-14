#!/usr/bin/python3
"""command module of executor"""
from os import access as _access, environ as _environ, \
    getuid as _getuid, X_OK as _X_OK
from sys import \
    stdout as _stdout, \
    stdout as _stderr
__echo = _stdout.write
__puke = _stderr.write

from socket import getfqdn as _fqdn
from subprocess import call as _call, Popen as _Popen, PIPE as _PIPE

# for subprocess version compatibility while DEVNULL is new in subprocess
try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = open('/dev/null')


class Command(object):
	"""command execution class"""
	_sh_ = False
	_su_ = False
	_dbg = False
	def __init__(self, *args):
		for arg in args:
			arg = '_%s_'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		if self.dbg:
			print(Command.__mro__)
	# rw properties
	@property               # sh_ <bool>
	def sh_(self):
		return self._sh_
	@sh_.setter
	def sh_(self, val):
		self._sh_ = val if val else False

	@property               # su_ <bool>
	def su_(self):
		return self._su_
	@su_.setter
	def su_(self, val):
		self._su_ = val if val else False

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if val else False

	@staticmethod
	def __which(prog):
		"""pretty much like the `which` command (see `man which`)"""
		for path in _environ['PATH'].split(':'):
			if _access('%s/%s'%(path, prog), _X_OK):
				return '%s/%s'%(path, prog)

	def __list(self, commands):
		"""
		commands string to list converter assuming at least one part
		"""
		for cmd in list(commands):
			if cmd and max(len(c) for c in cmd) == 1 and len(cmd) >= 1:
				return list(commands)
			return self.__list(list(cmd))
		#cmds = []
		#try:
		#	cmds = eval(commands)
		#except (SystemError, TypeError):
		#	#print(commands)
		#	for cmmd in commands:
		#		if isinstance(cmmd, str):
		#			if ' ' in cmmd:
		#				for cmd in cmmd.split(' '):
		#					cmds.append(cmd)
		#			else:
		#				cmds.append(cmmd)
		#		else:
		#			for cmd in cmmd:
		#				cmds.append(cmd)
		#return list(cmds)

	@staticmethod
	def __str(commands):
		"""list/tuple to str converter"""
		print(commands)
		return ' '.join(str(command) for command in list(commands))

	@staticmethod
	def __sucmd(sudobin, commands):
		if 'sudo' in commands[0]:
			del commands[0]
		if int(_getuid()) != 0:
			commands.insert(0, sudobin)
		return commands

	def _sudo(self, commands=None):
		"""privilege checking function"""
		sudo = self.__which('sudo')
		if not commands:
			if int(_call([sudo, '-v'])) == 0:
				return True
			sucmds = None
		else:
			sucmds = self.__sucmd(sudo, commands)
		return sucmds

	def __cmdprep(self, commands):
		commands = self.__list(commands)
		if self.su_:
			commands = self._sudo(commands)
		if self.sh_:
			commands = self.__str(commands)
		if self.dbg:
			print('\033[01;30m`%s`\t{sh: %s, su: %s}\033[0m'%(commands, self.sh_, self.su_))
		return commands

	def run(self, *commands):
		"""just run the command and return the processes PID"""
		commands = self.__cmdprep(commands)
		return _Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, *commands):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		commands = self.__cmdprep(commands)
		return int(_call(commands, shell=self.sh_))

	def stdx(self, *commands):
		"""command execution which returns STDERR and/or STDOUT"""
		commands = self.__cmdprep(commands)
		prc = _Popen(commands, stdout=_PIPE, stderr=_PIPE, shell=self.sh_)
		out, err = prc.communicate()
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, *commands):
		"""command execution which returns STDOUT only"""
		commands = self.__cmdprep(commands)
		prc = _Popen(commands, stdout=_PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate()
		if out:
			return out.decode()

	def stde(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands)
		prc = _Popen(commands, stdout=_PIPE, stderr=_PIPE, shell=self.sh_)
		_, err = prc.communicate()
		if err:
			return err.decode()

	def erno(self, *commands):
		"""command execution which returns the exitcode only"""
		commands = self.__cmdprep(commands)
		prc = _Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate()
		return int(prc.returncode)

	def oerc(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands)
		prc = _Popen(commands, stdout=_PIPE, stderr=_PIPE, shell=self.sh_)
		out, err = prc.communicate()
		return out.decode(), err.decode(), int(prc.returncode)


command = Command('sh')
sucommand = Command('sh', 'su')

def sudofork(*args):
	enr = 0
	try:
		enr = sucommand.call(*args)
	except KeyboardInterrupt:
		print('\n\033[34maborted by keystroke\033[0m')
	finally:
		exit(enr)



if __name__ == '__main__':
	exit(0)
