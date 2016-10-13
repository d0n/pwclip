#!/usr/bin/env python3

from os.path import expanduser

from cmd import Cmd

from datetime import date as datetime

from ssl import create_default_context

from getpass import getpass

import readline

from http.cookiejar import CookieJar, MozillaCookieJar, LoadError

from urllib.request import build_opener, HTTPSHandler, HTTPCookieProcessor

from urllib.parse import urlencode

from lxml import html

from system import stamp, userfind

from colortext import bgre, error

class LoginFailedError(Exception): pass

class Satan(object):
	_dbg = None
	url = 'https://login.1and1.org/ims-sso/login?service=' \
        'http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort'
	username = userfind()
	password = None
	_date = str(datetime.today())
	_dates = _date.split('-')
	_year = _dates[0]
	_month = _dates[1]
	_day = _dates[2]
	casslpem = expanduser('~/.config/catrust/ssl.pem')
	def __init__(self, *args, **kwargs):
		self._dbg = True if 'dbg' in args else self._dbg
		self.username = self.username if (
            'username' not in kwargs.keys()) else kwargs['username']
		self.password = self.password if (
            'password' not in kwargs.keys()) else kwargs['password']
		self.casslpem = self.casslpem if (
            'casslpem' not in kwargs.keys()) else kwargs['casslpem']
		self.day = self.day if 'day' not in kwargs.keys() else self.day
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
		self.cj = CookieJar()
		self.cxt = create_default_context(cafile=self.casslpem)
		self.browser = build_opener(
            HTTPCookieProcessor(self.cj),
            HTTPSHandler(debuglevel=0,context=self.cxt))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val

	@property                # year <int>
	def year(self):
		return int(self._year)
	@year.setter
	def year(self, val):
		self._year = val if isinstance(val, int) and val > 2000 else self._year

	@property                # month <int>
	def month(self):
		return int(self._month)
	@month.setter
	def month(self, val):
		self._month = val if isinstance(val, int) and val < 13 else self._month

	@property                # day <str>
	def day(self):
		return int(self._day)
	@day.setter
	def day(self, val):
		self._day = val if isinstance(val, int) and val < 32 else self._day

	@property                # date <str>
	def date(self):
		return str(self._date)
	@date.setter
	def date(self, val):
		try:
			self._date = val
			self.dates = val
			self.year = val.split('-')[0]
			self.month = val.split('-')[1]
			self.day = val.split('-')[2]
		except (IndexError, AttributeError):
			self._date = str(datetime.today())
			self.dates = self._date
			self.year = self._date.split('-')[0]
			self.month = self._date.split('-')[1]
			self.day = self._date.split('-')[2]
			

	@property                # dates <tuple>
	def dates(self):
		return self._dates
	@dates.setter
	def dates(self, val):
		try:
			self._dates = tuple(int(i) for i in reversed(self.date.split('-')))
		except ValueError:
			self.date = str(datetime.today())
			self._dates = tuple(int(i) for i in reversed(str(datetime.today()).split('-')))

	def _login(self):
		if self.dbg:
			print(bgre(self._login))
		__passwd = self.password
		if not __passwd:
			__passwd = getpass('enter password for %s: '%self.username)
		tree = html.fromstring(self.browser.open(self.url).read())
		form = tree.find('.//form')
		response = self.browser.open(self.url,
                urlencode({"username": self.username,
                    "password": __passwd,
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
				self.url = self.browser.open(self.url).geturl()
			else:
				print(res.decode())
				raise LoginFailedError()
		#self.weekefforts()

	def _todate_(self, url, date):
		setattr(self, 'date', date)
		self.browser.open(
            url,
            urlencode({"__from": "%02d.%02d.%d"%self.dates}).encode())

	def _book_(self, duration, project, task, comment='', date=None):
		if self.dbg:
			print(bgre('%s\nd=%s, p=%s, t=%s, c=%s, %s'%(
			    self._book_, duration, project, task, comment, date)))
		self._todate_(self.url, self.date)
		code = urlencode({
            "__from": "%02d.%02d.%d"%self.dates,
            "__handler": \
                "handler.enter/effort.effortenterhandler#%02d%02d%d"%self.dates,
            "usage": "",
            "duration": duration,
            "project": project,
            "task": task,
            "comment": comment}).encode()
		_effort = self.browser.open(self.url, code)
		response = _effort.read()
		if response.find('Success'.encode()) == -1:
			raise Exception(
                'Enter effort failed - ' \
                'string "Success" not found.\nPOSTed:\n' \
                '---%s---\n\nResponse:\n---%s---\n\n'%(
                code.decode(), response.decode()))
			return True

	def weekefforts(self, week=0):
		if self.dbg:
			print(bgre(self.weekefforts))
		url = '%s/personal/view/week'%self.url.split('/enter/effort')[0]
		print(url)
		code = urlencode({"week": "%d"%week}).encode()
		tree = html.fromstring(self.browser.open(url, code).read())
		for tr in tree.xpath('tbody'):
			print(tr)

	def bookeffort(self, **kwargs):
		if self.dbg:
			print(bgre('%s\n  %s'%(self.bookeffort, tabd(kwargs))))
		for m in {'duration', 'project','task'}:
			assert kwargs[m] is not None
		return self._book_(**kwargs)



class TimeSatan(Cmd, Satan):
	prompt = '%s>> '%str(datetime.today())
	def __init__(self, *args, **kwargs):
		print('TimeSatan - book efforts to fuck-up-tool timsato\n' \
            '  empty line ends booking efforts')
		Cmd.__init__(self)
		Satan.__init__(self, *args, **kwargs)
		self._login()

	@property                # dbg <type>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = (val is True)

	@staticmethod
	def __exit(eof=False, msg='satan appreciates'):
		msg = msg if not eof else '\n%s'%msg
		print(msg)
		return True

	@staticmethod
	def _test_duration(dur):
		try:
			h = int(dur)
			m = 0
		except ValueError:
			h = dur
			m = 0
			if ':' in dur:
				try:
					h = int(dur.split(':')[0])
					m = int(dur.split(':')[1])
				except ValueError:
					return False
		try:
			return ((h <= 23) and (m <= 59 ))
		except TypeError:
			return False

	@staticmethod
	def _test_date(date):
		try:
			y, m, d = date.split('-')
			len(y) == 4
			len(m) in (1, 2)
			len(d) in (1, 2)
		except ValueError:
			return False
		return True

	def complete(self, text, state):
		"""Return the next possible completion for 'text'.
		If a command has not been entered, then complete against command list.
		Otherwise try to call complete_<command> to get list of completions.
		"""
		if state == 0:
			origline = readline.get_line_buffer()
			line = origline.lstrip()
			stripped = len(origline) - len(line)
			begidx = readline.get_begidx() - stripped
			endidx = readline.get_endidx() - stripped
			if begidx>0:
				cmd, args, foo = self.parseline(line)
				if cmd == '':
					compfunc = self.completedefault
				else:
					try:
						compfunc = getattr(self, 'complete_' + cmd)
					except AttributeError:
						compfunc = self.completedefault
			else:
				compfunc = self.completenames
			self.completion_matches = compfunc(text, line, begidx, endidx)
		try:
			if len(self.completion_matches) <= 1:
				return '%s '%self.completion_matches[state]
			return self.completion_matches[state]
		except IndexError:
			return None

	#def completedefault(self, text, line, begidx, endidx):
	#	return [text]
	def default(self, line, margs={}):
		__e = {
            'duration': 1,
            'comment': '',
            'task': 'sa.srm',
            'project': 'p.nod.mw'}
		__e.update(**margs)
		if self.dbg:
			print(bgre('%s\n  line = %s\n  %s'%(self.default, line, __e)))
		frags = line.split()
		if len(frags) > 1:
			__d = frags[-1]
			if not self._test_duration(__d):
				if __d == 'EOF':
					return self.__exit(True)
				return error(
                    'need duration', __d, 'is not')
			__e['duration'] = __d
			if len(frags) > 1 and not __e['comment']:
				__e['comment'] = ' '.join(frags[:-1])
		elif len(frags) == 1:
			if self._test_duration(line) and not __e['comment']:
				__e['comment'] = 'DailyWork'
				__e['duration'] = line
			elif self._test_date(line):
				return self.do_today(line)
			else:
				__e['comment'] = line
		elif not line:
			if [v for v in __e.values() if not v]:
				print(v)
			return error('missing input')
		self._book_(**__e)

	def do_today(self, line):
		self._todate_(self.url, line)
		self.prompt = '%s>> '%line

	def do_list(self, line):
		frags = line.split()
		if len(frags) > 1:
			return error('list does only accept the "day" argument, got',
                frags)
		elif len(frags) == 1:
			self.do_today(frags[0])
			return self.weekefforts()
		self.weekefforts()
	def do_l(self, line):
		self.do_list(line)

	def do_administration(self, line):
		__e = {'task': 'sa.srm',
            'project': 'p.nod.mw'}
		if len(line.split()) == 1:
			line = '%s 1'%line
		self.default(line)
	def do_admin(self, line):
		self.do_administration(line)
	def do_a(self, line):
		self.do_administration(line)

	def do_project(self, line):
		__e = {'task': 'sa.srm'}
		frags = line.split()
		if len(frags) >= 2:
			if not self._test_duration(frags[0]):
				__p = frags[0]
				if __p.isdigit():
					__e['project'] = 'ACC.%s'%__p
				elif __p and __p.lower().startswith('acc.'):
					__e['project'] = __p.upper()

		return self.default(' '.join(frags[1:]), __e)
	def do_p(self, line):
		self.do_project(line)

	def do_train(self, line):
		__e = {'task': 'train', 'project': 'p.nod2'}
		if len(line.split()) < 2:
			return error('comment missing, got', __e, line)
		self.default(line, __e)

	def do_jourfixe(self, line):
		__e = {'task': 'jf', 'project': 'p.nod2'}
		if len(line.split()) < 1:
			line = 'JourFixe 0:30'
		self.default(line, __e)
	def do_jf(self, line):
		self.do_jourfixe(line)
	def do_j(self, line):
		self.do_jourfixe(line)

	def do_meet(self, line, margs={}):
		__e = {'task': 'meet', 'project': 'p.nod2'}
		__e.update(**margs)
		if not len(line.split()) > 1:
			if self._test_duration(line.split()[-1]):
				if not 'comment' in __e.keys():
					return error('comment missing, got', __e)
			line = '1 %s'%line
		self.default(line, margs=__e)
	def do_teammeeting(self, line):
		if len(line) == 0:
			line = '1'
		self.do_meet('Teammeeting %s'%line)
	def do_t(self, line):
		self.do_teammeeting(line)
	def do_m(self, line):
		self.do_meet(line)

	def do_incident(self, line):
		__e = {'project': 'p.nod.mw', 'task': 'sa.ossinc'}
		if len(line.split()) == 1:
			line = '%s 1'%line
		if not line.lower().startswith('inc'):
			line = 'INC-%s'%line
		return self.default(line, __e)
	def do_inc(self, line):
		self.do_incident(line)
	def do_i(self, line):
		self.do_incident(line)

	def emptyline(self):
		return self.__exit()




if __name__ == '__main__':
	satan = TimeSatan()
	satan.mainloop()
