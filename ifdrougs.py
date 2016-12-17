from system import which
from executor import command as c, sucommand as s
from net.network import isup

def dhclient(iface, verbose=True):
	dhclient = which('dhclient')
	if verbose:
		x = s.call
	else:
		x = s.erno
	if int(x(dhclient+' -v '+iface)) == 0:
		return True

def ifup(iface, dhcp=True):
	ifup = which('ifup')
	if not dhcp:
		ifup = '%s --no-scripts'%(ifup)
	out, err, eno = s.oerc('%s %s'%(ifup, iface))
	err = err.strip()
	if eno == 0 and not err.startswith('Ignoring'):
		return True

def ifdown(iface):
	out, err, eno = s.oerc('%s %s'%(which('ifdown'), iface))
	if eno == 0:
		out, err = out.strip(), err.strip()
		if err.endswith('not configured'):
			if ifconfdown(iface):
				return True
		elif not out and not err:
			return True
		elif ((not out and eno == 0) or \
              (out.endswith('...done.') and eno == 0) or \
			  (out.endswith('ntp.service.') and eno == 0)):
			return True
		else:
			print('out = %s\nerr = %s\nnum = %s\n' %(out, err, eno))


def ifconfup(iface):
	if s.erno('%s %s up'%(which('ifconfig'), iface)) == 0:
		return True

def ifconfdown(iface):
	out, err, eno = s.oerc('%s %s down' %(which('ifconfig'), iface))
	if not isup(iface) and not out and not err and eno == 0:
		return
	if eno == 0:
		return True
	else:
		err = 'ifconfig down %s %s' %(iface, err)
		raise RuntimeError(err)

def ping(domain='www.google.de', count=1, wait=1):
	if int(c.erno(
		  '%s -c%s -W%s %s'%(which('ping'), count, wait, domain))) == 0:
		return True


