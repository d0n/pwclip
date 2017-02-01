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
from os import \
    remove, makedirs
from os.path import \
    isdir, expanduser
import sys
from tempfile import mkstemp

from executor import command

cfghead = """
# --- BEGIN custom openssl.cnf ---
HOST                = {fqdn}
RANDFILE            = {rnd}
oid_section         = new_oids

[ new_oids ]

[ req ]
default_days        = {expire}
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
	outdir = expanduser(cfgvals['outdir'])
	if not isdir(outdir):
		makedirs(outdir)
	if not isdir('%s/csr'%outdir):
		makedirs('%s/csr'%outdir)
	keyoutfile = '%s/%s'%(outdir, cfgvals['keyfile']) if (
        'keyfile' in cfgvals.keys()) else '%s/%s-key.pem'%(outdir, fqdn)
	csroutfile = '%s/%s'%(outdir, cfgvals['csrfile']) if (
        'csrfile' in cfgvals.keys()) else '%s/csr/%s-csr.pem'%(outdir, fqdn)
	config = '%s%s%s'%(cfghead, cfgbody, cfgtail)
	cfgvals['fqdn'] = fqdn
	cfgvals['keyfile'] = keyoutfile
	cfgvals['rnd'] = expanduser('~/.rnd')
	#print(config)
	#print(cfgvals)
	#print(names)
	if names:
		cfgvals['altnames'] = 'DNS:%s'%', DNS:'.join(n for n in names)
		config = '%s%s%s%s%s'%(cfghead, cfgreqs, cfgbody, cfgalts, cfgtail)
	_, tmpfile = mkstemp(prefix='openssl-conf.')
	config = config.format(**cfgvals)
	#print(config)
	with open(tmpfile, 'w+') as tmpcfg:
		tmpcfg.write(config)
	command.call(
        'openssl req -batch -config %s -newkey rsa:4096 -sha512 -out %s'%(
            tmpfile, csroutfile))
	remove(tmpfile)









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
