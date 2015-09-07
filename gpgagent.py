def agentinfo(user):
	agentinfo = '/home/%s/.gnupg/agent.env'%user
	with open(agentinfo, 'r') as agi:
		return dict((k.split(';')[0].strip(), v.split(';')[0].strip()) for (k, v) in dict(line.split('=') for line in agi.readlines()).items())

