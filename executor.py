#!/usr/bin/python3
"""command module of executor"""
from os import access as _access, environ as _environ, \
    getuid as _getuid, X_OK as _X_OK

from sys import \
    stdout as _stdout, \
    stdout as _stderr
_echo_ = _stdout.write
_puke_ = _stderr.write

from subprocess import call as _call, Popen as _Popen, PIPE as _PIPE
# for legacy subprocess compatibility while DEVNULL is new in subprocess
try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = open('/dev/null')

class Command(object):
	_sh_ = True
	_su_ = False
	_dbg = False
	_tout_ = None
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
			elif hasattr(self, '%s_'%arg):
				setattr(self, '%s_'%arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '%s_'%key):
				setattr(self, '%s_'%key, val)
		if self.dbg:
			lim = int(max(len(k) for k in Command.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                Command.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(Command.__dict__.items())),
                Command.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	# rw properties
	@property               # sh_ <bool>
	def sh_(self):
		return self._sh_
	@sh_.setter
	def sh_(self, val):
		self._sh_ = val

	@property               # su_ <bool>
	def su_(self):
		return self._su_
	@su_.setter
	def su_(self, val):
		self._su_ = val

	@property                # tout <int>
	def tout(self):
		return self._tout
	@tout.setter
	def tout(self, val):
		self._tout = val if isinstance(val, int) else self._tout

	@staticmethod
	def __which(prog):
		"""pretty much like the `which` command (see `man which`)"""
		for path in _environ['PATH'].split(':'):
			if _access('%s/%s'%(path, prog), _X_OK):
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
		return _Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, *commands):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		commands = self.__cmdprep(commands, self.call)
		return int(_call(commands, shell=self.sh_))

	def stdx(self, *commands):
		"""command execution which returns STDERR and/or STDOUT"""
		commands = self.__cmdprep(commands, self.stdx)
		prc = _Popen(commands, stdout=_PIPE, stderr=_PIPE, shell=self.sh_)
		out, err = prc.communicate(timeout=self._tout_)
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, *commands):
		"""command execution which returns STDOUT only"""
		commands = self.__cmdprep(commands, self.stdo)
		prc = _Popen(commands, stdout=_PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate(timeout=self._tout_)
		if out:
			return out.decode()

	def stde(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands, self.stde)
		prc = _Popen(commands, stdout=_PIPE, stderr=_PIPE, shell=self.sh_)
		_, err = prc.communicate(timeout=self._tout_)
		if err:
			return err.decode()

	def erno(self, *commands):
		"""command execution which returns the exitcode only"""
		commands = self.__cmdprep(commands, self.erno)
		prc = _Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate(timeout=self._tout_)
		return int(prc.returncode)

	def oerc(self, *commands):
		"""command execution which returns STDERR only"""
		commands = self.__cmdprep(commands, self.oerc)
		prc = _Popen(
            commands, stdout=_PIPE, stderr=_PIPE, stdin=_PIPE, shell=self.sh_)
		out, err = prc.communicate(timeout=self._tout_)
		return out.decode(), err.decode(), int(prc.returncode)


command = Command('sh')
sucommand = Command('sh', 'su')

def sudofork(*args):
	enr = 0
	try:
		enr = sucommand.call(args)
	except KeyboardInterrupt:
		_echo_('\n\033[34maborted by keystroke\033[0m\n')
	finally:
		exit(enr)



if __name__ == '__main__':
	exit(0)
