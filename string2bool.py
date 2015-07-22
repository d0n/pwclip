def string2bool(varstr):
	varstr = str(varstr).lower()
	if varstr in ('false', 'disabled', '0'):
		return False
	elif varstr in ('true', 'enabled', '1'):
		return True
	elif varstr in ('none', '', [], {}):
		return None
	else:
		return varstr

