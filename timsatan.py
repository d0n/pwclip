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

<<<<<<< HEAD

class TimeSatan(object):
	_dbg = True
	username = userfind()
	password = None
	casslpem = _expanduser('.config/pukirootca.pem')
	def __init__(self, *args, **kwargs):
		self.username = self.username if (
            'username' not in kwargs.keys()) else kwargs['username']
		self.password = _getpass('enter password for %s: '%self.username) if (
            'password' not in kwargs.keys()) else kwargs['password']
		self.casslpem = self.casslpem if (
		    'casslpem' not in kwargs.keys()) else kwargs['casslpem']
=======
# local imports
from colortext import bgre, tabd

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
		elif not self.__passwd:
			self.__passwd = _getpass('enter password for %s: '%self.username)
>>>>>>> 6817e469157067440f9688f63279f7b4589cb532
		cj = _CookieJar()
		cxt = _create_default_context(cafile=self.casslpem)
		self.opener = _build_opener(
                _HTTPCookieProcessor(cj),
                _HTTPSHandler(debuglevel=0,context=cxt))
<<<<<<< HEAD
		home = self.opener.open('https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort')
		tree = _html.fromstring(home.read())
		form = tree.find('.//form')
		post = self.opener.open('https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort',
                _urlencode({"username": user,
                    "password": password,
                    "lt": form.find('.//input[@name="lt"]').value,
                    "execution": form.find('.//input[@name="execution"]').value,
                    "_eventId": form.find('.//input[@name="_eventId"]').value,
                    "submit": form.find('.//input[@name="submit"]').value}))
		#print(post.read())
		if post.geturl().startswith('https://login.1and1.org/'):
			if post.read().find('Invalid credentials'):
				raise Exception('Login failed')
			else:
				raise Exception('Forward to timsato failed')
		self.curday = _date.today()
		self.url = post.geturl()
		if self.dbg:
			lim = int(max(len(k) for k in Test.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                Test.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(Test.__dict__.items())),
                Test.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))
=======
		home = self.opener.open(self.url)
		tree = _html.fromstring(home.read())
		form = tree.find('.//form')
		_post = self.opener.open(self.url,
                _urlencode({"username": self.username,
                    "password": self.__passwd,
                    "lt": form.find('.//input[@name="lt"]').value,
                    "execution": form.find('.//input[@name="execution"]').value,
                    "_eventId": form.find('.//input[@name="_eventId"]').value,
                    "submit": form.find('.//input[@name="submit"]').value
                }).encode())
		purl, post = _post.geturl(), _post.read()
		if purl.startswith('https://login.1and1.org/'):
			invcrd = post.find("Invalid credentials".encode())
			if post.find("Invalid credentials".encode()) != -1:
				raise LoginFailedError(
                    'Login failed (invalid credentials) %s'%invcrd)
			elif post.find("Change password".encode()) != -1:
				print('password change required')
			else:
				print(post.decode())
				raise LoginFailedError()
		self.curday = _date.today()
>>>>>>> 6817e469157067440f9688f63279f7b4589cb532
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
<<<<<<< HEAD
		self._dbg = True if val else False

	def work(self, day, duration, project, task, comment=''):
		date_t = (day.day, day.month, day.year)

		#strange: if you book for past days you have to 'post' the __from for this day
		#to be able to book the first section
		if self.curday != day:
			#print('curday ' + str(self.curday) + ' differs from ' + str(day) + ' post __from first')
			set_day = self.opener.open(self.url, _urlencode({"__from": "%02d.%02d.%d" % date_t}))
			self.curday = day

		encode = urlencode({"__from": "%02d.%02d.%d"%date_t,
			"__handler": "handler.enter/effort.effortenterhandler#%02d%02d%d" % date_t,
			"usage": "",
			"duration": duration,
			"project": project,
			"task": task,
			"comment": comment,
			})
		enter_effort = self.opener.open(self.url, encode)
		html_resp = enter_effort.read()
		#print(html_resp)
		if html_resp.find('Success') == -1:
			raise Exception('Enter effort failed - string "Success" not found.\nPOSTed: ' + encode)

	def bookfromconfig(self, day):
		for section in self.config.sections():
			if 'daily' in section:
				self.booksection(day,section)
			if day.strftime('%A').lower() in section:
				self.booksection(day,section)

	def booksection(self, day, section):
		sect = {}
		isok = True
		for mandatory in ['duration', 'project','task']:
			try:
				sect[mandatory] =  self.config.get(section, mandatory)
			except ConfigParser.Error:
				print('SKIP: ' + section + ' - mandatory field "' + mandatory + '" missing')
				isok = False
		try:
			sect['comment'] = self.config.get(section, 'comment')
		except ConfigParser.Error:
			sect['comment'] = ''
		if isok:
			#print('book section "' + section + '" with:')
			#self.printdictionary(sect)
			self.work(day, sect['duration'], sect['project'], sect['task'], sect['comment'])

	def workdaysfromconfig(self, begin, end):
		for o in range(begin.toordinal(), end.toordinal() + 1):
			day = _date.fromordinal(o)
			if day.isoweekday() <= 5:
				print(day)
				self.bookfromconfig(day)

	def printdictionary(self, items):
		for key in items.keys():
			print(' ' + key + ': ' + items[key])


#f = Filler()
#book single work-targets with:
#f.work(date.today(), '0:01', 'p.toh8.xxxxxxxxxxx', 'sa', 'auto')
#f.work(date(2015, 12, 27), '0:01', 'p.toh8.xxxxxxxxxxx', 'sa', 'auto')
#
#book single day from configfile:
#f.bookfromconfig(date.today())
#f.bookfromconfig(date(2015, 12, 27))
#
#book range of workdays from configfile
#f.workdaysfromconfig(date(2015, 12, 23), date.today())
=======
		self._dbg = val

	def __login_(self):
		if 'password' in kwargs.keys():
			self.__passwd = kwargs['password']
		elif not self.__passwd:
			self.__passwd = _getpass('enter password for %s: '%self.username)
		cj = _CookieJar()
		cxt = _create_default_context(cafile=self.casslpem)
		self.opener = _build_opener(
                _HTTPCookieProcessor(cj),
                _HTTPSHandler(debuglevel=0,context=cxt))
		home = self.opener.open(self.url)
		tree = _html.fromstring(home.read())
		form = tree.find('.//form')
		_post = self.opener.open(self.url,
                _urlencode({"username": self.username,
                    "password": self.__passwd,
                    "lt": form.find('.//input[@name="lt"]').value,
                    "execution": form.find('.//input[@name="execution"]').value,
                    "_eventId": form.find('.//input[@name="_eventId"]').value,
                    "submit": form.find('.//input[@name="submit"]').value
                }).encode())
		purl, post = _post.geturl(), _post.read()
		if purl.startswith('https://login.1and1.org/'):
			invcrd = post.find("Invalid credentials".encode())
			if post.find("Invalid credentials".encode()) != -1:
				raise LoginFailedError(
                    'Login failed (invalid credentials) %s'%invcrd)
			elif post.find("Change password".encode()) != -1:
				print('password change required')
			else:
				print(post.decode())
				raise LoginFailedError()


	def _book_(self, duration, project, task, day=None, comment=''):
		#
		# day, duration, project, task, comment=''
		#
		# strange: if you book for past days you have to 'post'
		# the __from for this day to be able to book the first section
		if self.dbg:
			print(bgre(self._book_))
		day = day if day else self.curday
		__d = (day.day, day.month, day.year)
		if day and self.curday != day:
			self.opener.open(
                self.url,
                _urlencode({"__from": "%02d.%02d.%d"%__d}))
			self.curday = day
		code = _urlencode({
            "__from": "%02d.%02d.%d"%__d,
            "__handler": \
                "handler.enter/effort.effortenterhandler#%02d%02d%d"%__d,
            "usage": "",
            "duration": duration,
            "project": project,
            "task": task,
            "comment": comment})
		_effort = self.opener.open(self.url, code.encode())
		response = _effort.read()
		if response.find('Success'.encode()) == -1:
			raise Exception(
                'Enter effort failed - ' \
                'string "Success" not found.\nPOSTed: %s'%code)
		return True

	def bookeffort(self, **kwargs):
		if self.dbg:
			print(bgre('%s\n  %s'%(self.bookeffort, tabd(kwargs))))
		for m in {'duration', 'project','task'}:
			assert kwargs[m] is not None
		return self._book_(**kwargs)






if __name__ == '__main__':
	exit(1)
>>>>>>> 6817e469157067440f9688f63279f7b4589cb532
