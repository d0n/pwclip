from system import which
from executor import command as c

def rfklist(devnum=None):
	rfkill = which('rfkill')
	devlist = {}
	devlocks = []
	if rfkill:
		rfklist = c.stdo(rfkill+' list')
		if rfklist:
			for line in rfklist.split('\\n'):
				if line and line[1] == ':':
					device = line.split()[1]
					if device.endswith(':'):
						device = device[:-1]
				elif line.startswith('\\t'):
					locktyp = line.split('\\t')[1].split(' ')[0].lower()
					islock = line.split('\\t')[1].split(' ')[-1]
					devlocks.append({locktyp:islock})
				if len(devlocks) == 2:
					devlist[device] = devlocks
					devlocks = []
	if devlist != {}:
		return devlist

def rfklocks(rfklst=rfklist()):
	lockdevs = []
	if rfklst:
			for device in rfklst:
					for locks in rfklst[device]:
							for lock in locks:
									if locks[lock] == 'yes':
											lockdevs.append({device:lock})
	if lockdevs != []:
			return lockdevs
