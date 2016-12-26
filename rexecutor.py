from system import which
from system.user import whoami
from executor.executor import Command

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
	_host_ = ''
	_user_ = whoami()
	_tout_ = 30
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
			elif hasattr(self, '%s_'%key):
				setattr(self, '%s_'%key, val)
		if self.dbg:
			lim = int(max(len(k) for k in SSHCommand.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                SSHCommand.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(SSHCommand.__dict__.items())),
                SSHCommand.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
		super().__init__(*args, **kwargs)

	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	@property                # host_ <str>
	def host_(self):
		return self._host_
	@host_.setter
	def host_(self, val):
		self._host_ = val

	@property                # user_ <str>
	def user_(self):
		return self._user_
	@user_.setter
	def user_(self, val):
		self._user_ = val

	@property                # tout <int>
	def tout(self):
		return self._tout
	@tout.setter
	def tout(self, val):
		self._tout = val if isinstance(val, int) else self._tout

	def _hostcmd(self, *commands, host=None, user=None):
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
		return ssh + self._list(commands)

	def run(self, *commands, host=None, user=None):
		commands = self._hostcmd(*commands, host=host, user=user)
		return super().run(*commands)

	def call(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().call(commands)

	def stdx(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stdx(commands)

	def stdo(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stdo(commands)

	def stde(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().stde(commands)

	def erno(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().erno(commands)

	def oerc(self, *commands, host=None, user=None):
		commands = self._hostcmd(commands, host, user)
		return super().oerc(commands)
