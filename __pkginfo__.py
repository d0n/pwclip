#!/usr/bin/env python3
"""pwclip packaging information"""
name = 'pwclip'
version = '.'.join([str(num) for num in (1, 3, 1)])
provides = ['pwcli', 'pwclip', 'ykclip']
install_requires = [
    'argcomplete', 'netaddr', 'paramiko', 'psutil',
    'pyusb', 'python-gnupg', 'python-yubico', 'PyYAML', 'wget']
license = 'GPL'
description = "gui to temporarily save passwords to system-clipboard"
url = 'https://pypi.org/project/pwclip/%s/'%version
author = 'Leon Pelzer'
author_email = 'mail@leonpelzer.de'
download_url = 'https://pypi.python.org/pypi/pwclip/%s#downloads'%version
classifiers = ['Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Security',
               'Topic :: Utilities',
               'Topic :: Desktop Environment',
               'Topic :: System :: Systems Administration']
include_package_data = True
try:
	with open('docs/CHANGELOG.rst', 'r') as cfh:
		__changes = '\n\n\n'.join(cfh.read().split('\n\n\n')[:4])
except OSError:
	__changes = ''
try:
	with open('docs/README.rst', 'r') as rfh:
		__readme = rfh.read().format(ChangeLog=__changes)
except OSError:
	__readme = ''
long_description = (__readme)
with open('README', 'w+') as wfh:
	wfh.write(__readme)
entry_points = {
    'gui_scripts': ['pwclip = pwclip.__init__:pwclip',
                    'ykclip = pwclip.__init__:ykclip'],
    'console_scripts': ['pwcli = pwclip.__init__:pwcli']}
package_data = {
    '': ['pwclip/docs/*.rst']}
data_files=[
    ('share/man/man1', ['pwclip/docs/pwclip.1']),
    ('share/pwclip', [
        'pwclip/example/ca.crt', 'pwclip/example/commands.lst',
        'pwclip/example/ssl.crt', 'pwclip/example/ssl.key',
        'pwclip/example/example_passwords.yaml'])]
