from sys import \
    stderr as _stderr
from os import \
    stat as _stat
from stat import \
    S_ISSOCK as _ISSOCK

def agentinfo(user):
	stdsock = '/home/%s/.gnupg/S.gpg-agent.ssh' 
	if user == 'root':
		stdsock = '/root/.gnupg/S.gpg-agent.ssh'
	if _ISSOCK(_stat(stdsock).st_mode):
		return stdsock
	agentinfo = '/home/%s/.gnupg/agent.env'%user
	try:
		with open(agentinfo, 'r') as agi:
			return dict(line.split(';')[0].split('=') for line in agi.readlines())
			#return dict((k.split(';')[0].strip(), v.split(';')[0].strip()) for (k, v) in dict(line.split('') for line in agi.readlines()).items())
	except FileNotFoundError as err:
		print(err, file=_stderr)

