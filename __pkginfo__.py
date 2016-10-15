"""pwclip packaging information"""
import sys
from os.path import join

modname = distname = 'pwclip'
numversion = (0, 0, 3)
version = '.'.join([str(num) for num in numversion])
install_requires = [
    'pyusb',
    'yubico']
license = 'GPL'
description = "secure-password-hash-clipper (copy/paste) via challenge-response"
web = 'http://janeiskla.de'
mailinglist = ""
author = 'Leon Pelzer'
author_email = 'mail@leonpelzer.de'
classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Debuggers',
               'Topic :: Software Development :: Quality Assurance',
               'Topic :: Software Development :: Testing']


long_desc = """\
  provides a multi-platform password-hashing using yubikey challenge-response 
  and time-based access to that password-hash via System copy/paste buffers
  """
scripts = [join('bin', 'pwclip')]
entry_points={'console_scripts': ['pwclip = pwclip.__main__:main']}
