"""which module to find executables"""
from os import X_OK, access, environ, join as pjoin

def which(prog):
	"""which function like the linux 'which' program"""
	for path in environ['PATH'].split(':'):
		if access(pjoin(path, prog), X_OK):
			return pjoin(path, prog)
