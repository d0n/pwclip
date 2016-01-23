from sys import \
    stderr as _stderr
from os import \
    environ as _environ, \
    stat as _stat
from stat import \
    S_ISSOCK as _ISSOCK

def agentinfo(user):
	stdsock = '/home/%s/.gnupg/S.gpg-agent.ssh' 
	if user == 'root':
		stdsock = '/root/.gnupg/S.gpg-agent.ssh'
	elif 'SSH_AUTH_SOCK' in _environ.keys():
		stdsock = _environ['SSH_AUTH_SOCK']
	if _ISSOCK(_stat(stdsock).st_mode):
		return stdsock
	print(stdsock)
	agentinfo = '/home/%s/.gnupg/agent.env'%user
	try:
		with open(agentinfo, 'r') as agi:
			return dict(
                line.split(';')[0].split('=') for line in agi.readlines())
	except FileNotFoundError as err:
		return

