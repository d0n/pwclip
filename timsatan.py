# -*- coding: utf-8 -*-
#
from os.path import \
    expanduser as _expanduser

from datetime import \
    date as _date

from ssl import \
    create_default_context as _sslcontext

from lxml import \
    html as _html

from urllib import \
    urlencode as _urlencode

from urllib2 import \
    HTTPCookieProcessor as _HTTPCookieProcessor, \
    HTTPSHandler as _HTTPSHandler, \
    build_opener as _opener

from cookielib import \
    CookieJar as _CookieJar


class TimeSatan(object):
	_dbg = False
    _url = 'https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort'
	_usr = ''
	_pwd = ''
	_cfgs = {
        'username': self.usr, 'password': self.pwd,
        'lt': form.find('.//input[@name="lt"]').value,
        'execution': form.find('.//input[@name="execution"]').value,
        '_eventId': form.find('.//input[@name="_eventId"]').value,
        'submit': form.find('.//input[@name="submit"]').value}


	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
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
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True

	@property                # url <str>
	def url(self):
		return self._url

	@property                # usr <str>
	def usr(self):
		return self._usr
	@usr.setter
	def usr(self, val):
		self._usr = val if isinstance(val, str) else self._usr

	@property                # pwd <str>
	def pwd(self):
		return self._pwd
	@pwd.setter
	def pwd(self, val):
		self._pwd = val if isinstance(val, str) else self._pwd

	def _webmagic_(self):
		cookjar = _CookieJar()
		sslcntx = _sslcontext(cafile=self.cfgs['ssl'])
		__satan = _opener(
            _HTTPCookieProcessor(cookjar),
            _HTTPSHandler(debuglevel=0,context=sslcntx))
		hell = __satan.open(self.url, _urlencode(self.cfgs))
