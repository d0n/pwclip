from socket import getfqdn as __getfqdn, gethostbyname as __host


def _etchostname():
	with open('/etc/hostname', 'r') as hnf:
		return hnf.read()
	

def hostname(host=None, fqdn=None, net=None):
	if not host:
		host = _etchostname()
	if fqdn:
		host = __getfqdn(host)
	elif net:
		host = __host(host)
	return host.strip()
