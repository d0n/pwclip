def main():
    #gpgmemods()
    #_gpgme.make_constants(globals())
    d0n = gpg.get_key(_fingerprint('d0nkey'))
    lpz = gpg.get_key(_fingerprint('d0nkey'))
    plain = io.BytesIO(b'geh-heim')

    crypt.seek(0)

    plain = io.BytesIO()

    gpg.decrypt(crypt, plain)

    print(plain.getvalue())

    #print(dir(usrkey))
    #print(usrkey.secret)
    #with open('hashs.db', 'r') as inf, open('hashdb.gpg', 'w') as off:
    #   gpg.encrypt([usrkey], 0, inf, off)

