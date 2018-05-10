======
pwclip
======

.. include:: ./description.rst

========
Synopsis
========

**pwcli** *[-h] [--version] [-D] [-A] [-o] [-s] [-t seconds] [-R]*
          *[--remote-host HOST] [--remote-user USER] [-r "ID ..."] [-u USER]*
          *[-p PWD] [--comment COM] [-x] [-C SSL-Certificate]*
          *[-K SSL-Private-Key] [--ca SSL-CA-Certificate] [-P CRYPTFILE]*
          *[-Y YAMLFILE] [-S {1,2}] [-y [SERIAL]] [-a ENTRY] [-c ENTRY]*
          *[-d ENTRY [ENTRY ...]] [-l [PATTERN]]*

=======
Options
=======

.. program:: pwclip

.. option::    --version

    show program's version number and exit

.. option::    -D, --debug

    debugging mode

.. option::    -A, --all

    switch to all users entrys ("d0n" only is default)

.. option::    -o, --stdout

    print password to stdout (insecure and unrecommended)

.. option::    -s, --show-passwords

    show passwords when listing (replaced by "*" is default)

.. option::    -t seconds

    time to wait before resetting clip (3 is default)

.. option::    -p PWD, --password PWD

    enter password for add/change actions (insecure & not recommended)

.. option::    --comment COM

    enter comment for add/change actions

.. option::    -R

    use remote backup given by --remote-host

.. option::    --remote-host HOST

    use HOST for connections

.. option::    --remote-user USER

    use USER for connections to HOST ("d0n" is default)

.. option::    -r "ID ...", --recipients "ID ..."

    one ore more gpg-key ID(s) to use for encryption (strings seperated by spaces within "")

.. option::    -u USER, --user USER

    query entrys only for USER (-A overrides, "d0n" is default)

.. option::    -x, --x509

    force ssl compatible gpgsm mode - usually is autodetected (use --cert & --key for imports)

.. option::   -C SSL-Certificate, --cert SSL-Certificate

    one-shot setting of SSL-Certificate

.. option::   -K SSL-Private-Key, --key SSL-Private-Key

    one-shot setting of SSL-Private-Key

.. option::   --ca SSL-CA-Certificate, --ca-cert SSL-CA-Certificate

    one-shot setting of SSL-CA-Certificate

.. option::   -P CRYPTFILE, --passcrypt CRYPTFILE

    set location of CRYPTFILE to use as password store (~/.passcrypt is default)

.. option::   -Y YAMLFILE, --yaml YAMLFILE

    set location of YAMLFILE to read whole sets of passwords from a yaml file (~/.pwd.yaml is default)

.. option::   -S {1,2}, --slot {1,2}

    set one of the two yubikey slots (only useful with -y)

.. option::   -y [SERIAL], --ykserial [SERIAL]

    switch to yubikey mode and optionally set SERIAL of yubikey (autoselect serial and slot is default)

.. option::   -a ENTRY, --add ENTRY

    add ENTRY (password will be asked interactivly)

.. option::   -c ENTRY, --change ENTRY

    change ENTRY (password will be asked interactivly)

.. option::   -d ENTRY [ENTRY ...], --delete ENTRY [ENTRY ...]

    delete ENTRY(s) from the passcrypt list

.. option::   -l [PATTERN], --list [PATTERN]

    pwclip an entry matching PATTERN if given - otherwise list all entrys


.. include:: ./usage.rst


.. include:: ./troubleshoot.rst


.. include:: ./credits.rst


.. seealso:: :manpage:`gnupg(1)`, :manpage:`python(1)`

