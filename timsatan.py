#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from datetime import \
    date as _date

from ssl import \
    create_default_context as _sslcontext

from lxml import \
    html as _html

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
	_url = 'https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort'
	_cokj = ''
	_sslc = ''
	username = ''
	password = ''
	cacert = ''
	def __init__(self, *args, **kwargs):
		for arg in args:
			#arg = '_%s'%(arg)
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
	@property                # url <str>
	def url(self):
		return self._url

	@property                # cokj <CookieJar>
	def cokj(self):
		if not self._cpkj:
			self._cokj = _CookieJar()
		return self._cokj

	@property                # sslc <create_default_context>
	def sslc(self):
		if not self._sslc:
			self._sslc = _sslcontext(cacert=self.cacert)
		return self._sslc

	def _urlopen_(self):
		return _opener(
            _HTTPCookieProcessor(self.cokj),
            _HTTPSHandler(debuglevel=0,context=self.sslc))

	def _post_(self):
		__satan = _opener(
            _HTTPCookieProcessor(self.cokj),
            _HTTPSHandler(debuglevel=0, context=self.sslc))
		_hell = __satan.open(self.url, _urlencode(self.cfgs))
		_tree = _html.fromstring(_hell.read())
		_form = _tree.find('.//form')
		_post = __satan.open(self.url)











if __name__ == '__main__':
	exit(1)
