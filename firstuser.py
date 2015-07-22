
def firstuser(uid='1000', gid=None): #, pattern=None):
	gid = gid if gid else uid
	with open('/etc/passwd', 'r') as pwd:
		return [
                 l.split(':')[0] for l in pwd.readlines() \
                 if l.split(':')[2] == uid and l.split(':')[3] == gid
                ]
