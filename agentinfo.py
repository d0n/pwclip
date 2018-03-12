from os import environ, stat as osstat

from stat import S_ISSOCK as issock

from system.user import userfind

def gpgagentinfo(user=None):
	uid = int(userfind(userfind(), 'uid'))
	usrhome = userfind(uid, 'home')
	gpgsock = '%s/.gnupg/S.gpg-agent'%usrhome
	sshsock = '%s/.gnupg/S.gpg-agent.ssh'%usrhome
	if (
          not issock(osstat(gpgsock).st_mode) or \
          not issock(osstat(sshsock).st_mode)):
		rundir = '/run/user/%d/gnupg'%uid
		gpgsock = '%s/S.gpg-agent'%rundir
		sshsock = '%s/S.gpg-agent.ssh'%rundir
	environ['GPG_AGENT_INFO'] = '%s:0:1'%gpgsock
	environ['SSH_AUTH_SOCK'] = sshsock
	return gpgsock, sshsock
