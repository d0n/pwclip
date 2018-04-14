pwclip
======

Synopsis
--------
usage: pwcli [-h] [--version] [-D] [-A] [-o] [-s] [-t seconds] [-R]
             [--remote-host HOST] [--remote-user USER] [-r IDs] [-u USER] [-x]
             [-C SSL-Certificate] [-K SSL-Private-Key]
             [--ca SSL-CA-Certificate] [-P CRYPTFILE] [-Y YAMLFILE] [-S {1,2}]
             [-y [SERIAL]] [-a ENTRY] [-c ENTRY] [-d ENTRY [ENTRY ...]]
             [-l [PATTERN]]

Description
-----------

pwclip - multi functional password manager to temporarily save passphrases to
your copy/paste buffers for easy and secure accessing your passwords

Options
-------
.. program:: pwcli

.. option::   -A, --all

   switch to all users entrys (instead of current user only)

.. option::   -o, --stdout

   print received password to stdout (insecure & unrecommended)

.. option::   -s, --show-passwords

   switch to display passwords (replaced with * by default)

.. option::   -t seconds

   time to wait before resetting clip (default is 3 max 3600)

.. option::   -R

   use remote backup given by --remote-host

.. option::   --remote-host HOST

   use HOST for connections

.. option::   --remote-user USER

   use USER for connections to HOST

.. option::   -r ID(s), --recipients ID(s)

   gpg-key ID(s) to use for encryption (string seperated by spaces)

.. option::   -u USER, --user USER

   query entrys only for USER (defaults to current user, overridden by -A)

.. option::   -x, --x509

   force ssl compatible gpgsm mode - usually is autodetected (use --cert
   --key for imports)

.. option::   -C SSL-Certificate, --cert SSL-Certificate

   one-shot setting of SSL-Certificate

.. option::   -K SSL-Private-Key, --key SSL-Private-Key

   one-shot setting of SSL-Private-Key

.. option::   --ca SSL-CA-Certificate, --ca-cert SSL-CA-Certificate

   one-shot setting of SSL-CA-Certificate

.. option::   -P CRYPTFILE, --passcrypt CRYPTFILE

   set location of CRYPTFILE to use for gpg features

.. option::   -Y YAMLFILE, --yaml YAMLFILE

   set location of one-time password YAMLFILE to read & delete

.. option::   -S {1,2}, --slot {1,2}

   set one of the two slots on the yubi-key (only useful for -y)

.. option::   -y [SERIAL], --ykserial [SERIAL]

   switch to yubikey mode and optionally set SERIAL of yubikey

.. option::   -a ENTRY, --add ENTRY

   add ENTRY (password will be asked interactivly)

.. option::   -c ENTRY, --change ENTRY

   change ENTRY (password will be asked interactivly)

.. option::   -d ENTRY [ENTRY ...], --delete ENTRY [ENTRY ...]

   delete ENTRY(s) from the passcrypt list

.. option::   -l [PATTERN], --list [PATTERN]

   search entry matching PATTERN if given otherwise list all


Examples
--------

    $ pwcli -P .mycrypt -Y pwds.yaml -C myrottensslcert.pem -K myrottensslkey.pem -A -l
      # merges and lists passwords using ssl

.. seealso::

   :manpage:`gnupg(1)`, :manpage:`python(1)`
