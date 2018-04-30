"""pwclip packaging information"""
name = 'pwclip'
version = None
with open('./docs/CHANGELOG.rst', 'r') as cfh:
    version = [l for l in cfh.readlines() if '(current)' in l]
version = "0.0.1" if not version else version[0].split('(current)')[0]
provides = ['pwcli', 'pwclip', 'ykclip']
install_requires = [
    'argcomplete', 'netaddr', 'paramiko', 'psutil',
    'pyusb', 'python-gnupg', 'python-yubico', 'PyYAML', 'wget']
description = "gui to temporarily save passwords to system-clipboard"
url = 'https://pypi.org/project/pwclip/'
author = 'Leon Pelzer'
author_email = 'mail@leonpelzer.de'
download_url = 'http://deb.janeiskla.de/ubuntu/pool/main/p/pwclip/python3-pwclip_%s-1_all.deb'%version
classifiers = ['Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: GNU General Public License',
               'Operating System :: OS Independent',
               'Programming Language :: Python3',
               'Topic :: Security',
               'Topic :: Utilities',
               'Topic :: Passwords',
               'Topic :: Password Management',
               'Topic :: Desktop Environment']
include_package_data = True
long_description = ''
try:
	long_description = '\n\n\n'.join(
        str(open('pwclip/docs/CHANGELOG.rst', 'r').read()).split('\n\n\n')[:4])
except FileNotFoundError:
	long_description = ''
try:
	long_description = str(
        open('pwclip/docs/README.rst', 'r').read()
        ).format(ChangeLog=long_description)
except FileNotFoundError:
	long_description = ''
if long_description:
	open('README', 'w+').write(long_description)
entry_points = {
    'console_scripts': ['pwcli = pwclip.__init__:pwcli'],
    'gui_scripts': ['pwclip = pwclip.__init__:pwclip',
                    'ykclip = pwclip.__init__:ykclip']}
package_data = {
    '': ['pwclip/docs/'],
    '': ['pwclip/example']
	}
data_files=[
    ('share/man/man1', ['pwclip/docs/pwclip.1']),
    ('share/pwclip', [
        'pwclip/example/ca.crt', 'pwclip/example/commands.lst',
        'pwclip/example/ssl.crt', 'pwclip/example/ssl.key',
        'pwclip/example/passwords.yaml'])]
