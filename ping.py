from system import which
from executor import command as cmd

def ping(domain='www.google.de', count=1, wait=1):
	if int(cmd.erno(
          '%s -c%s -W%s %s'%(which('ping'), count, wait, domain))) == 0:
		return True
