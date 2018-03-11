from os import environ, stat as osstat

from system.user import userfind

def gpgagentinfo(user=None):
	uid = int(userfind(userfind(), 'uid'))
	rundir = '/run/user/%d/gnupg'%uid
	#gpgsock, sshsock = '%s/S.gpg-agent'%rundir, '%s/S.gpg-agent.ssh'%rundir
	gpgsock, sshsock = '%s/S.gpg-agent:0:1'%rundir, '%s/S.gpg-agent.ssh'%rundir
	environ['GPG_AGENT_INFO'] = gpgsock
	environ['SSH_AUTH_SOCK'] = sshsock
	return gpgsock, sshsock
