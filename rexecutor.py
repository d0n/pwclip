from system import which
from system.user import whoami
from executor.executor import Command

class SSHCommand(Command):
	dbg = False
	sh_ = True
	su_ = False
	_sshbin = which('ssh')
	_sshopts = {
        'o': [
            'StrictHostKeyChecking=no',
            'UserKnownHostsFile=/dev/null', 'LogLevel=ERROR'],
        '4': None
        }
	host_ = ''
	user_ = whoami()
	tout_ = 30
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
		Command.__init__(self, *args, **kwargs)

	def _hostcmd(self, *commands, host=None, user=None):
		"""ssh host prepending function"""
		if not user:
			user = self.user_
		if not host:
			host = self.host_
		self._sshopts['l'] = user
		ssh = [self._sshbin]
		for (key, vals) in self._sshopts.items():
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
		#print(ssh + self._list(commands))
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
