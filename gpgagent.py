def agentinfo(user):
	agentinfo = '/home/%s/.gnupg/gpg-agent.info'%user
	with open(agentinfo, 'r') as agi:
		return dict((k.strip(), v.strip()) for (k, v) in dict(line.split('=') for line in agi.readlines()).items())

