#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from datetime import \
    date as _date

from ssl import \
    create_default_context as _sslcontext

from lxml.html import \
    fromstring as _fromstring

from urllib.parse import \
    urlencode as _urlencode

from urllib.request import \
    build_opener as _opener, \
    HTTPSHandler as _HTTPSHandler, \
    HTTPCookieProcessor as _HTTPCookieProcessor

from http.cookiejar import \
    CookieJar as _CookieJar

class TimeSatan(object):
	dbg = False
	_url = 'https://login.1and1.org/ims-sso/login?' \
        'service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort'
	crt = ''
	usr = ''
	pwd = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in TimeSatan.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                TimeSatan.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(TimeSatan.__dict__.items())),
                TimeSatan.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # url <str>
	def url(self):
		return self._url

	def _hell_(self):
		return _opener(
                _HTTPCookieProcessor(_CookieJar()),
                _HTTPSHandler(
                    debuglevel=0,
                    context=_sslcontext(cafile=crt)))

	def _login(self):
		_satan = self._hell_.open(self.url)
		_fire = _fromstring(_satan.read()).find('.//form')
		_pain = self._hell_.open(self.url, _urlencode({
            'username': self.usr,
            'password': self.pwd,
            'lt': _fire.find('.//input[@name="lt"]').value,
            'execution': _fire.find('.//input[@name="execution"]').value,
            '_eventId': _fire.find('.//input[@name="_eventId"]').value,
            'submit': _fire.find('.//input[@name="submit"]').value}))
		if _pain.geturl().startswith('https://login.1and1.org/'):
			if post.read().find('Invalid credentials'):
				raise RuntimeError('Login failed')
			else:
				raise RuntimeError('Forward to timsato failed')
		return _pain.geturl()


	def _book_(self, day, duration, project, task, comment=''):
		_date = ()
		pass



if __name__ == '__main__':
	exit(1)
