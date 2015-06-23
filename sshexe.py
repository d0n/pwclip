from systools import which, whoami
from .executor import Command
class SSHCommand(Commad):
    _user_ = logduser()

	@property                # user_ <str>
	def user_(self):
		return self._user_
	@user_.setter
	def user_(self, val):
		self._user_ = val if type(val) is str else self._user_

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

