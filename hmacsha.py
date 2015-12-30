from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random.random import getrandbits
from Crypto.Util import Counter

EXPANSION_COUNT = (10000, 10000, 100000)
AES_KEY_LEN = 256
SALT_LEN = (128, 256, 256)
HASH = SHA256
PREFIX = b'sc'
HEADER = (PREFIX + b'\x00\x00', PREFIX + b'\x00\x01', PREFIX + b'\x00\x02')
LATEST = 2   # index into SALT_LEN, EXPANSION_COUNT, HEADER

# lengths here are in bits, but pcrypto uses block size in bytes
HALF_BLOCK = AES.block_size*8//2
for salt_len in SALT_LEN:
    assert HALF_BLOCK <= salt_len  # we use a subset of the salt as nonce

HEADER_LEN = 4
for header in HEADER:
    assert len(header) == HEADER_LEN


def enhmacsha(password, data):
    data = _str_to_bytes(data)
    _assert_encrypt_length(data)
    salt = bytes(_random_bytes(SALT_LEN[LATEST]//8))
    hmac_key, cipher_key = _expand_keys(password, salt, EXPANSION_COUNT[LATEST])
    counter = Counter.new(HALF_BLOCK, prefix=salt[:HALF_BLOCK//8])
    cipher = AES.new(cipher_key, AES.MODE_CTR, counter=counter)
    encrypted = cipher.encrypt(data)
    hmac = _hmac(hmac_key, HEADER[LATEST] + salt + encrypted)
    return HEADER[LATEST] + salt + encrypted + hmac


def dehmacsha(password, data):
    _assert_not_unicode(data)
    _assert_header_prefix(data)
    version = _assert_header_version(data)
    _assert_decrypt_length(data, version)
    raw = data[HEADER_LEN:]
    salt = raw[:SALT_LEN[version]//8]
    hmac_key, cipher_key = _expand_keys(password, salt, EXPANSION_COUNT[version])
    hmac = raw[-HASH.digest_size:]
    hmac2 = _hmac(hmac_key, data[:-HASH.digest_size])
    if _assert_hmac(hmac_key, hmac, hmac2): return
    counter = Counter.new(HALF_BLOCK, prefix=salt[:HALF_BLOCK//8])
    cipher = AES.new(cipher_key, AES.MODE_CTR, counter=counter)
    plain = cipher.decrypt(raw[SALT_LEN[version]//8:-HASH.digest_size])
    return plain #.decode()



class DecryptionException(Exception): pass
class EncryptionException(Exception): pass

def _assert_not_unicode(data):
    u_type = type(b''.decode('utf8'))
    if isinstance(data, u_type):
        raise DecryptionException(
            'data to decrypt must be bytes; you cannot use a string ' \
            'because no string encoding will accept all possible characters.')

def _assert_encrypt_length(data):
    if len(data) > 2**HALF_BLOCK:
        raise EncryptionException('message too long.')

def _assert_decrypt_length(data, version):
    if len(data) < HEADER_LEN + SALT_LEN[version]//8 + HASH.digest_size:
        raise DecryptionException('missing data.')

def _assert_header_prefix(data):
    if len(data) >= 2 and data[:2] != PREFIX:
        raise DecryptionException(
            'could not read header (bad header)')

def _assert_header_version(data):
    if len(data) >= HEADER_LEN:
        try:
            return HEADER.index(data[:HEADER_LEN])
        except:
            raise DecryptionException(
                'could not read header (bad header)')
    else:
        raise DecryptionException('missing header')

def _assert_hmac(key, hmac, hmac2):
     if _hmac(key, hmac) != _hmac(key, hmac2):
        return False

def _pbkdf2(password, salt, n_bytes, count):
    return PBKDF2(password, salt, dkLen=n_bytes,
        count=count, prf=lambda p,s: HMAC.new(p,s,HASH).digest())

def _expand_keys(password, salt, expansion_count):
    if not salt: raise ValueError('missing salt')
    if not password: raise ValueError('missing password')
    key_len = AES_KEY_LEN // 8
    keys = _pbkdf2(_str_to_bytes(password), salt, 2*key_len, expansion_count)
    return keys[:key_len], keys[key_len:]

def _hide(ranbytes):
    return bytearray(_pbkdf2(bytes(ranbytes), b'', len(ranbytes), 1))

def _random_bytes(n):
    return _hide(bytearray(getrandbits(8) for _ in range(n)))

def _hmac(key, data):
    return HMAC.new(key, data, HASH).digest()

def _str_to_bytes(data):
    u_type = type(b''.decode('utf-8'))
    if isinstance(data, u_type):
        return data.encode('utf-8')
    return data
