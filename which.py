import os
def which(prog):
	for path in os.environ['PATH'].split(':'):
		if os.access('%s/%s'%(path, prog), os.X_OK):
			return '%s/%s'%(path, prog)

