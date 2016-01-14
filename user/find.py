from sys import stderr as _stderr

def userfind(pattern='1000', mode='user'):
	"""
        >>> 0 = name
        >>> 1 = x
        >>> 2 = uid
        >>> 3 = gid
        >>> 4 = comment
        >>> 5 = home
        >>> 6 = shell
	"""
	user = 0
	x = 1
	uid = 2
	gid = 3
	comment = 4
	home = 5
	shell = 6
	mode = int(eval(mode))
	pstr = str(pattern)
	try:
		with open('/etc/passwd', 'r') as pwd:
			hits = [f.split(':') for f in [l for l in pwd.readlines() if pstr in l] if pstr in f][0]
			#hits = [
            #    l.split(':') for l in [
            #        l.strip() for l in pwd.readlines()] if str(pattern) in l]
	except PermissionError as err:
		print(err, file=sys.stderr)
		return err
	if hits:
		return list(hits)[mode]
