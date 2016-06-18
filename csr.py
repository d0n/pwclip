#!/usr/bin/env python3
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""module disclaimer"""

# global & stdlib imports
#import re
from os import \
    remove as _remove, \
    makedirs as _makedirs

from os.path import \
    isdir as _isdir, \
    expanduser as _expanduser

import sys
from tempfile import mkstemp

# local relative imports
from executor import command as c

# global default variables
__version__ = '0.0'

cfghead = """
# --- BEGIN custom openssl.cnf ---
HOST                = {fqdn}
RANDFILE            = {rnd}
oid_section         = new_oids

[ new_oids ]

[ req ]
default_days        = {days}
default_keyfile     = {keyfile}
distinguished_name  = req_distinguished_name
encrypt_key         = no
string_mask         = nombstr"""

cfgreqs = """
req_extensions      = v3_req"""

cfgbody = """

[ req_distinguished_name ]
C                   = {country}
L                   = {location}
commonName          = {organisation}
commonName_default  = {fqdn}

[ v3_req ]"""


cfgalts = """
subjectAltName      = {altnames}"""

cfgtail = """
# --- END custom openssl.cnf ---"""



def csrgen(fqdn, *names, **cfgvals):
	"""
	expire=730,
	country='DE', location='KA',
	organisation='1&1 Internet AG',
	orgunit='Middleware Operations',
	outdir='~/wrk/ssl', keyfile=None, csrfile=None):
	ugly, dirty, evil csr template generating and openssl forking function
	"""
	outdir = _expanduser(cfgvals['outdir'])
	if not _isdir(outdir):
		_makedirs(outdir)
	if not _isdir('%s/csr'%outdir):
		_makedirs('%s/csr'%outdir)
	keyoutfile = '%s/%s'%(outdir, cfgvals['keyfile']) if (
        'keyfile' in cfgvals.keys()) else '%s/%s-key.pem'%(outdir, fqdn)
	csroutfile = '%s/%s'%(outdir, cfgvals['csrfile']) if (
        'csrfile' in cfgvals.keys()) else '%s/csr/%s-csr.pem'%(outdir, fqdn)
	cfgvals = {
        'fqdn': fqdn, 'days': cfgvals['expire'],
        'rnd': _expanduser('~/.rnd'),
        'country': cfgvals['country'], 'location': cfgvals['location'],
        'organisation': cfgvals['organisation'],
        'keyfile': keyoutfile, 'orgunit': cfgvals['unit']}
	config = '%s%s%s'%(cfghead, cfgbody, cfgtail)
	#print(names)
	if names:
		cfgvals['altnames'] = 'DNS:%s'%', DNS:'.join(*names)
		config = '%s%s%s%s%s'%(cfghead, cfgreqs, cfgbody, cfgalts, cfgtail)
	_, tmpfile = mkstemp(prefix='openssl-conf.')
	config = config.format(**cfgvals)
	#print(config)
	with open(tmpfile, 'w+') as tmpcfg:
		tmpcfg.write(config)
	c.call('openssl req -batch -config %s -newkey rsa:4096 -sha512 -out %s'%(
        tmpfile, csroutfile))
	_remove(tmpfile)









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
