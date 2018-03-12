from os import environ, stat as osstat

from stat import S_ISSOCK as issock

from system.user import userfind

def gpgagentinfo(user=None):
	uid = int(userfind(userfind(), 'uid'))
	rundir = '/run/user/%d/gnupg'%uid
	gpgsock = '%s/S.gpg-agent'%rundir
	sshsock = '%s/S.gpg-agent.ssh'%rundir
	if not issock(osstat(gpgsock).st_mode):
		usrhome = userfind(uid, 'home')
		gpgsock = '%s/.gnupg/S.gpg-agent'%usrhome
		sshsock = '%s/.gnupg/S.gpg-agent.ssh'%usrhome
	environ['GPG_AGENT_INFO'] = gpgsock
	environ['SSH_AUTH_SOCK'] = sshsock
	return gpgsock, sshsock
