#!/usr/bin/env python3

from os.path import \
    expanduser as _expanduser

from getpass import \
    getpass as _getpass

from http.cookiejar import \
    CookieJar as _CookieJar

from ssl import \
    create_default_context as _create_default_context

from urllib.request import \
    build_opener as _build_opener, \
    HTTPSHandler as _HTTPSHandler, \
    HTTPCookieProcessor as _HTTPCookieProcessor

from urllib.parse import \
    urlencode as _urlencode

from lxml import \
    html as _html

from datetime import \
    date as _date

from system.user import userfind

class LoginFailedError(Exception): pass

class TimeSatan(object):
	_dbg = False
	opener = None
	url = 'https://login.1and1.org/ims-sso/login?service=' \
	    'http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort'
	username = userfind()
	__passwd = None
	casslpem = _expanduser('~/.config/catrust/ssl.pem')
	def __init__(self, *args, **kwargs):
		self._dbg = True if 'dbg' in args else self._dbg
		self.username = self.username if (
            'username' not in kwargs.keys()) else kwargs['username']
		self.casslpem = self.casslpem if (
		    'casslpem' not in kwargs.keys()) else kwargs['casslpem']
		if self.dbg:
			lim = int(max(len(k) for k in TimeSatan.__dict__.keys()))+4
			print(bgre('%s\n%s\n\n%s\n%s\n'%(
                TimeSatan.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(TimeSatan.__dict__.items())),
                TimeSatan.__init__,
                '\n'.join('  %s%s=    %s'%(k, ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()
                    ) if not k.startswith('_TimeSatan__')))))
		if 'password' in kwargs.keys():
			self.__passwd = kwargs['password']
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	def __login_(self):
		if self.dbg:
			print(bgre(self.__login_))
		if not self.__passwd:
			self.__passwd = _getpass('enter password for %s: '%self.username)
		cj = _CookieJar()
		cxt = _create_default_context(cafile=self.casslpem)
		self.opener = _build_opener(
            _HTTPCookieProcessor(cj),
            _HTTPSHandler(debuglevel=0,context=cxt))
		tree = _html.fromstring(self.opener.open(self.url).read())
		form = tree.find('.//form')
		response = self.opener.open(self.url,
                _urlencode({"username": self.username,
                    "password": self.__passwd,
                    "lt": form.find('.//input[@name="lt"]').value,
                    "execution": form.find('.//input[@name="execution"]').value,
                    "_eventId": form.find('.//input[@name="_eventId"]').value,
                    "submit": form.find('.//input[@name="submit"]').value
                }).encode())
		self.url, res = response.geturl(), response.read()
		if self.url.startswith('https://login.1and1.org/'):
			if res.find("Invalid credentials".encode()) != -1:
				raise LoginFailedError(
                    'Login failed (invalid credentials)')
			elif res.find("Change password".encode()) != -1:
				print('password change required')
				self.url = self.opener.open(self.url).geturl()
			else:
				print(res.decode())
				raise LoginFailedError()

	def _book_(self, duration, project, task, day=None, comment=''):
		if self.dbg:
			print(bgre(self._book_))
		day = day if day else self.curday
		__d = tuple(int(i) for i in reversed(str(day).split('-')))
		self.opener.open(
            self.url,
            _urlencode({"__from": "%02d.%02d.%d"%__d}).encode())
		code = _urlencode({
            "__from": "%02d.%02d.%d"%__d,
            "__handler": \
                "handler.enter/effort.effortenterhandler#%02d%02d%d"%__d,
            "usage": "",
            "duration": duration,
            "project": project,
            "task": task,
            "comment": comment}).encode()
		_effort = self.opener.open(self.url, code)
		response = _effort.read()
		if response.find('Success'.encode()) == -1:
			raise Exception(
                'Enter effort failed - ' \
                'string "Success" not found.\nPOSTed: %s'%code)
		return True

	def bookeffort(self, **kwargs):
		if self.dbg:
			print(bgre('%s\n  %s'%(self.bookeffort, tabd(kwargs))))
		self.__login_()
		for m in {'duration', 'project','task'}:
			assert kwargs[m] is not None
		return self._book_(**kwargs)






if __name__ == '__main__':
	exit(1)
