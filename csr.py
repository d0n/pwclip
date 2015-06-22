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
import os
import sys
from tempfile import mkstemp

# local relative imports
from executor import command as c

# global default variables
__version__ = '0.0'


def csrgen(fqdn, host, alters=[], outdir=os.path.expanduser('~/'),
           keyfile=None, csrfile=None, days=730, comname='1&1 Internet AG'):
	"""
	ugly, dirty, evil csr template generating and openssl forking function
	"""
	keyoutfile = '%s/%s'%(outdir, keyfile)
	if not keyfile:
		keyoutfile = '%s/%s-key.pem'%(outdir, fqdn)
	csroutfile = '%s/%s'%(outdir, csrfile)
	if not csrfile:
		csroutfile = '%s/%s-csr.pem'%(outdir, fqdn)
	cfgvals = {
	    'host': host, 'fqdn': fqdn, 'days': days,
	    'comname': comname, 'keyfile': keyoutfile}
	_, tmpfile = mkstemp(prefix='openssl-conf.')
	config = '# -------------- BEGIN custom openssl.cnf -----\n' \
	    'HOST                    = {host}\n'
	if os.uname()[0] == 'HP-UX':
		config = config + \
		    'RANDFILE                = %s\n'%os.path.expanduser('~/.rnd')
	config = config + \
	    'oid_section             = new_oids\n' \
	    '[ new_oids ]\n' \
	    '[ req ]\n' \
	    'default_days            = {days}\n' \
	    'default_keyfile         = {keyfile}\n' \
	    'distinguished_name      = req_distinguished_name\n' \
	    'encrypt_key             = no\n' \
	    'string_mask = nombstr\n'
	if alters:
		config = config + \
		    'req_extensions = v3_req\n'
	config = config + \
	    '[ req_distinguished_name ]\n' \
	    'commonName              = {comname}\n' \
	    'commonName_default      = {fqdn}\n' \
	    'commonName_max          = 64\n' \
	    '[ v3_req ]\n'
	if alters:
		cfgvals['altnames'] = 'DNS:%s'%',DNS:'.join(a for a in alters)
		config = config + \
		    'subjectAltName          = {altnames}\n'
	config = config + \
	    '# -------------- END custom openssl.cnf -----'
	with open(tmpfile, 'w+') as tmpcfg:
		tmpcfg.write(config.format(**cfgvals))
	c.call('openssl req -batch -config %s -newkey rsa:4096 -sha1 -out %s'%(
	    tmpfile, csroutfile))
	os.remove(tmpfile)









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))

