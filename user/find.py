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
	try:
		with open('/etc/passwd', 'r') as pwd:
			hits = [
                l.split(':') for l in [
                    l.strip() for l in pwd.readlines()] if str(pattern) in l]
	except PermissionError as err:
		print(err, file=sys.stderr)
		return err
	if hits:
		hits = list(set(
            [hit[mode] for hit in hits for h in hit if h == pattern]))

		if mode in (2, 3):
			hits = [int(h) for h in hits]
		if len(hits) >= 1:
			return hits[0]
		return hits
