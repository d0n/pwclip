from datetime import datetime

def stamp():
	now = datetime.now()
	return '%s.%s'%(now.date(), str(now.time()).split('.')[0])
