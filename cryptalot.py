""" init"""
import os
from getpass import getpass as _getpass

# local/relative imports
from .hmacsha import enhmacsha, dehmacsha

def main():
	"""main"""
	tocrypt = input('gimme file to encrypt:').strip()
	if not os.path.isfile(tocrypt):
		print('cannot encrypt non existing file')
		exit(1)
	print(enhsfile(tocrypt))
	print(dehsfile('%s.vault'%tocrypt))


def enhsfile(plainf):
	"""encrypt using hmachsha function"""
	passwd = _getpass('tell me ya secret:')
	plainf = os.path.expanduser(plainf)
	with open(plainf, 'rb') as bpf:
		stream = bpf.read()
	crypt = enhmacsha(passwd, stream)
	with open('%s.vault'%plainf, 'wb+') as vcf:
		vcf.write(crypt)
	return crypt


def dehsfile(cryptf):
	"""decrypt using hmachsha function"""
	passwd = _getpass('tell me ya secret:')
	cryptf = os.path.expanduser(cryptf)
	with open(cryptf, 'rb') as vcf:
		crypt = vcf.read()
	return dehmacsha(passwd, crypt).decode()


if __name__ == '__main__':
	exit(1)
