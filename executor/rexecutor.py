from system import which
from system.user import whoami
from executor.executor import Command

class SSHCommand(Command):
	sh_ = True
	su_ = False
	dbg = False
	sshbin = which('ssh')
	sshopts = {
        'o': [
            'StrictHostKeyChecking=no',
            'UserKnownHostsFile=/dev/null', 'LogLevel=ERROR']}
	remote = ''
	reuser = whoami()
	timeout = 30
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		Command.__init__(self, *args, **kwargs)

	def _remotecmd(self, *commands, remote=None, reuser=None):
		"""ssh remote prepending function"""
		reuser = reuser if reuser else self.reuser
		remote = remote if remote else self.remote
		assert remote != None
		self.sshopts['l'] = reuser
		ssh = [self.sshbin]
		for (key, vals) in self.sshopts.items():
			key = '-%s'%(key)
			if isinstance(vals, list):
				for val in vals:
					ssh.append(key)
					ssh.append(val)
				continue
			ssh.append(key)
			if vals:
				ssh.append(vals)
		ssh.append(remote)
		#print(ssh + self._list(commands))
		return ssh + self._list(commands)

	def run(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(*commands, remote=remote, reuser=reuser)
		return super().run(*commands)

	def call(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().call(commands)

	def stdx(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().stdx(commands)

	def stdo(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().stdo(commands)

	def stde(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().stde(commands)

	def erno(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().erno(commands)

	def oerc(self, *commands, remote=None, reuser=None):
		commands = self._remotecmd(commands, remote, reuser)
		return super().oerc(commands)
