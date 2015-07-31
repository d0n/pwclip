import os
def whoami():
	with open('/etc/passwd', 'r') as pwf:
		pwl = pwf.readlines()
	user = [u.split(':')[0] for u in pwl if int(u.split(':')[2]) == os.getuid()]
	if user:
		return user[0]

