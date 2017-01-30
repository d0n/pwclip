#!/usr/bin/python3
"""command module of executor"""
from os import access, environ, getuid, X_OK

from sys import stdout, stderr
_echo_ = stdout.write
_puke_ = stderr.write

from subprocess import call, Popen, PIPE
# for legacy subprocess compatibility while DEVNULL is new in subprocess
try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = open('/dev/null')

class Command(object):
	sh_ = True
	su_ = False
	dbg = False
	timeout = None
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '%s_'%arg):
				setattr(self, '%s_'%arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)

	@staticmethod
	def __which(prog):
		"""pretty much like the `which` command (see `man which`)"""
		for path in environ['PATH'].split(':'):
			if access('%s/%s'%(path, prog), X_OK):
				return '%s/%s'%(path, prog)

	def _list(self, commands):
		"""
		commands string to list converter assuming at least one part
		"""
		#print(commands)
		for cmd in list(commands):
			if cmd and max(len(c) for c in cmd if c) == 1 and len(cmd) >= 1:
				return list(commands)
			return self._list(list(cmd))

	@staticmethod
	def _str(commands):
		"""list/tuple to str converter"""
		#print(commands)
		return ' '.join(str(command) for command in list(commands))

	@staticmethod
	def __sucmd(sudobin, commands):
		if 'sudo' in commands[0]:
			del commands[0]
		if int(getuid()) != 0:
			commands.insert(0, sudobin)
		return commands

	def _sudo(self, commands=None):
		"""privilege checking function"""
		sudo = self.__which('sudo')
		if not commands:
			if int(call([sudo, '-v'])) == 0:
				return True
			sucmds = None
		else:
			sucmds = self.__sucmd(sudo, commands)
		return sucmds

	def __cmdprep(self, commands, func):
		commands = self._list(commands)
		if self.su_:
			commands = self._sudo(commands)
		if self.sh_:
			commands = self._str(commands)
		if self.dbg:
			_echo_('\033[01;30m%s\n  `%s`\t{sh: %s, su: %s}\033[0m\n'%(
                func, commands, self.sh_, self.su_))
		return commands

	def run(self, *commands):
		"""just run the command and return the processes PID"""
		commands = self.__cmdprep(commands, self.run)
		return Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, *commands):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		commands = self.__cmdprep(commands, self.call)
		return int(call(commands, shell=self.sh_))

	def stdx(self, *commands):
		"""command execution which returns STDERR and/or STDOUT"""
		commands = self.__cmdprep(commands, self.stdx)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate(timeout=self.timeout)
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, *commands):
		"""command execution which returns STDOUT only"""
		commands = self.__cmdprep(commands, self.stdo)
		prc = Popen(commands, stdout=PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate(timeout=self.timeout)
		if out:
			return out.decode()

	def stde(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands, self.stde)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		_, err = prc.communicate(timeout=self.timeout)
		if err:
			return err.decode()

	def erno(self, *commands):
		"""command execution which returns the exitcode only"""
		commands = self.__cmdprep(commands, self.erno)
		prc = Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate(timeout=self.timeout)
		return int(prc.returncode)

	def oerc(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands, self.oerc)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate(timeout=self.timeout)
		return out.decode(), err.decode(), int(prc.returncode)


command = Command('sh')
sucommand = Command('sh', 'su')

def sudofork(*args):
	try:
		print(args)
		eno = int(sucommand.call(args))
	except KeyboardInterrupt:
		_echo_('\033[34maborted by keystroke\033[0m\n')
		eno = 1
	return eno

if __name__ == '__main__':
	exit(1)
