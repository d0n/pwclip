#!/usr/bin/python3
"""executing (remote) commands module"""
import os
from socket import getfqdn as fqdn
from subprocess import call, Popen, PIPE #, DEVNULL
#from libs import which
DEVNULL = open('/dev/null')

class Command(object):
	"""(remote) command execution module"""
	_sh_ = False
	_su_ = False
	_dbg = False
	__sshbin = which('ssh')
	# default ssh options (usually we dont want a lib to be interactive)
	__sshopts = {
        'o': [
            'StrictHostKeyChecking=no',
            'UserKnownHostsFile=/dev/null', 'LogLevel=ERROR'],
        '4': None
        }
	user = whoami()
	host = ''
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

	@staticmethod
	def __list(*commands):
		"""commands to list converter"""
		cmds = []
		try:
			cmds = eval(commands)
		except (SystemError, TypeError):
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
		return ' '.join(str(command) for command in commands)

	@staticmethod
	def _sudo():
		"""privilege checking function"""
		if int(os.getuid()) != 0:
			if int(call([which('sudo'), '-v'])) == 0:
				return True

	def _hostcmd(self, commands, host, user):
		"""ssh host prepending function"""
		if not user:
			user = self.user
		self.__sshopts['l'] = user
		ssh = [self.__sshbin]
		for (key, vals) in self.__sshopts.items():
			key = '-%s'%(key)
			if isinstance(vals, list):
				for val in vals:
					ssh.append(key)
					ssh.append(val)
				continue
			ssh.append(key)
			if vals:
				ssh.append(vals)
		ssh.append(fqdn(host))
		return ssh + commands

	def _sudocmd(self, commands):
		"""sudo to cmd prepending function"""
		if 'sudo' in commands[0]:
			del commands[0]
		if self.host:
			if self.user != 'root' and self.su_:
				commands.insert(0, which('sudo'))
		else:
			if self._sudo():
				commands.insert(0, which('sudo'))
		return commands

	def run(self, commands, host=None, user=None):
		"""just run the command and return the processes PID"""
		commands = self.__list(*commands)
		if self.su_:
			commands = self._sudocmd(commands)
		if host or self.host:
			commands = self._hostcmd(
                commands,
                host if host else self.host,
                user if user else self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		return Popen(
            commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_).pid

	def call(self, commands, host=None, user=None):
		"""
		default command execution
		prints STDERR, STDOUT and returns the exitcode
		"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		return int(call(commands, shell=self.sh_))

	def stdx(self, commands, host=None, user=None):
		"""command execution which returns STDERR and/or STDOUT"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		if out:
			return out.decode()
		if err:
			return err.decode()

	def stdo(self, commands, host=None, user=None):
		"""command execution which returns STDOUT only"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		prc = Popen(commands, stdout=PIPE, stderr=DEVNULL, shell=self.sh_)
		out, _ = prc.communicate()
		if out:
			return out.decode()

	def stde(self, commands, host=None, user=None):
		"""command execution which returns STDERR only"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		_, err = prc.communicate()
		if err:
			return err.decode()

	def erno(self, commands, host=None, user=None):
		"""command execution which returns the exitcode only"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		prc = Popen(commands, stdout=DEVNULL, stderr=DEVNULL, shell=self.sh_)
		prc.communicate()
		return int(prc.returncode)

	def oerc(self, commands, host=None, user=None):
		"""command execution which returns STDERR only"""
		if host:
			self.host = host
		if user:
			self.user = user
		commands = list(self.__list(*commands))
		if self.su_:
			commands = self._sudocmd(commands)
		if self.host:
			commands = self._hostcmd(commands, self.host, self.user)
		if self.sh_:
			commands = self.__str(*commands)
		if self.dbg:
			print(
                'cmd =', commands, 'sh =', self.sh_,
                'su =', self.su_, 'host =', self.host, 'user =', self.user)
		prc = Popen(commands, stdout=PIPE, stderr=PIPE, shell=self.sh_)
		out, err = prc.communicate()
		return out.decode(), err.decode(), prc.returncode



if __name__ == '__main__':
	exit(0)
