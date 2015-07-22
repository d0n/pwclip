from system import which, whoami, hostname
from .executor import Command

class SSHCommand(Command):
	_dbg = False
	_sh_ = True
	_su_ = False
	__sshbin = which('ssh')
	__sshopts = {
        'o': [
            'StrictHostKeyChecking=no',
            'UserKnownHostsFile=/dev/null', 'LogLevel=ERROR'],
        '4': None
        }
	_host_ = hostname()
	_user_ = whoami()

	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%arg
			if hasattr(self, arg):
				setattr(self, arg[1:], True)
		for (key, val) in kwargs.items():
			key = '_%s_'%key
			if hasattr(self, key):
				setattr(self, key[1:], val)
		if self.dbg:
			print('\033[01;30m%s\033[0m'%SSHCommand.__mro__)
			for (key, val) in self.__dict__.items():
				print('\033[01;30m%s = %s\033[0m'%(key, val))

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg

	@property                # host_ <str>
	def host_(self):
		return self._host_
	@host_.setter
	def host_(self, val):
		self._host_ = val if type(val) is str else self._host_

	@property                # user_ <str>
	def user_(self):
		return self._user_
	@user_.setter
	def user_(self, val):
		self._user_ = val if type(val) is str else self._user_

	def _hostcmd(self, commands, host=None, user=None):
		"""ssh host prepending function"""
		if not user:
			user = self.user_
		if not host:
			host = self.host_
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
		ssh.append(host)
		return ssh + [c for c in commands]

	def run(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().run(*commands)

	def call(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().call(*commands)

	def stdx(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stdx(*commands)

	def stdo(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stdo(*commands)

	def stde(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stde(*commands)

	def erno(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().erno(*commands)

	def oerc(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().oerc(*commands)
