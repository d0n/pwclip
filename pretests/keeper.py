#!/usr/bin/env python3
from os import getcwd as _getcwd, listdir as _listdir, remove as _remove
from os.path import isfile as _isfile, basename as _basename

#from Crypto.Hash import HMAC as __hmac
import simplecrypt as _simplecrypt
#from hashlib import sha512 as _sha512

#mysum = 'keeper.py'
#with open('keeper.py', 'rb') as myself:
#    mysum = _sha512(myself.read()).hexdigest()
#    myself.seek(0)
#    mydig = _sha512(myself.read()).digest()
#print(__hmac.new(input().encode(), mysum.encode()).hexdigest())

def plainreplace(fromfile, tofile):
    with open(fromfile, 'r') as fof, open(tofile, 'wb+') as tof:
        try:
            tof.write(_simplecrypt.encrypt(input('enter encryption password for %s: '%(_basename(fromfile))), fof.read().encode('utf-8')))
        finally:
            _remove(fromfile)

def readcrypt(fromfile):
    with open(fromfile, 'rb') as cdat:
        plain = _simplecrypt.decrypt(input('enter shared password: '), cdat.read())
    try:
        return plain
    except KeyboardInterrupt:
        exit()

vault = '%s/vault'%_getcwd()
for path in _listdir(vault):
    path = '%s/%s'%(vault, path)
    if _isfile(path) and not path.endswith('.crypt'):
        plainreplace(path, '%s.crypt'%path)
        continue
    if _isfile(path):
        plain = readcrypt(path)
        if plain:
            print(plain.decode('utf-8'))
