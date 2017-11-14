from os import environ, stat
from stat import S_ISSOCK

def agentinfo(user):
	stdsock = '/home/%s/.gnupg/S.gpg-agent'
	if user == 'root':
		stdsock = '/root/.gnupg/S.gpg-agent'
	environ['GPG_AGENT_INFO'] = '%s:0:1'%stdsock
	environ['SSH_AUTH_SOCK'] = '%s.ssh'%stdsock
	return stdsock
