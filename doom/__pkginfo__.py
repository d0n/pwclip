# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
"""doom packaging information"""

modname = distname = 'doom'

numversion = (0, 0, 1)
version = '.'.join([str(num) for num in numversion])

install_requires = [
]

lic = 'GPL'
description = "local admin/management application"
web = ''
mailinglist = ""
author = 'd0n'
author_email = 'd0n@janeiskla.de'

classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Administrators',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: Linux',
               'Programming Language :: Python :: 3',
               'Topic :: Administration :: Scripting'
              ]


long_desc = """\
 doom is a handy and lightweight daemon implementation for 
 """

scripts = ['doom']

include_dirs = []
