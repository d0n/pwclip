"""pwclip packaging information"""
name = 'pwclip'
provides = ['pwcli', 'pwclip', 'ykclip']
version = '1.7.1'
install_requires = [
    'argcomplete', 'psutil', 'python-gnupg', 'PyGObject', 'yubico', 'PyYAML', 'wget']
url = 'https://github.com/d0n/pwclip'
download_url = 'http://deb.janeiskla.de/ubuntu/pool/main/p/pwclip/python3-pwclip_%s-1_all.deb'%version
license = "GPLv3+"
author = 'Leon Pelzer'
description = 'password-manager - temporarily saves passwords to the clipboard'
author_email = 'mail@leonpelzer.de'
classifiers = ['Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: OSI Approved :: ' \
                   'GNU General Public License v3 or later (GPLv3+)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Security',
               'Topic :: Security :: Cryptography',
               'Topic :: Desktop Environment',
               'Topic :: Utilities',
               'Topic :: Desktop Environment']
include_package_data = True
long_description = ''
try:
	long_description = '%s\n\n'%str('\n\n\n'.join(
         str(open('pwclip/docs/changelog.rst', 'r').read()).split('\n\n\n')[:4]
        )).format(CurrentVersion='%s (current)\n----------%s'%(
            version, '-'*len(version)))
except (FileNotFoundError, NotADirectoryError):
	long_description = ''
try:
	__rs = []
	with open('pwclip/docs/readme.rst', 'r') as __r:
		__rs = __r.readlines()
	fmt = {}
	for l in __rs:
		if l.startswith('{'):
			l = l.strip('{}')
			fname = 'pwclip/docs/%s.rst'%l
			with open(fname, 'r') nfh:
				fmt[l] = nfh.read()
	long_description = ''.join(__rs).format(**fmt)
except (FileNotFoundError, NotADirectoryError):
    long_description = ''
try:
	with open('pwclip/docs/conf.py', 'w+') as cfh:
		cfh.write(str(open(
            'pwclip/docs/conf.py.tmpl', 'r').read()
            ).format(VersionString=version))
except (FileNotFoundError, NotADirectoryError):
	pass
entry_points = {
    'console_scripts': ['pwcli = pwclip.__init__:pwcli'],
    'gui_scripts': ['pwclip = pwclip.__init__:pwclip',
                    'ykclip = pwclip.__init__:ykclip']}
package_data = {
    '': ['pwclip/docs/'],
    '': ['pwclip/example']}
data_files=[
    ('share/man/man1', ['pwclip/docs/pwclip.1']),
    ('share/pwclip', [
        'pwclip/example/ca.crt', 'pwclip/example/commands.rst',
        'pwclip/example/ssl.crt', 'pwclip/example/ssl.key',
        'pwclip/example/passwords.yaml'])]
