#!/usr/bin/env python2

import ssl
import ConfigParser
from os import path
import urllib2
from urllib import urlencode
import cookielib
from lxml import html
from datetime import date
import getpass
#
#print(dir(ssl))

class Filler:
  def __init__(self):
    self.config = ConfigParser.ConfigParser()
    self.config.read(path.expanduser('~/.timsato'))

    try:
      user =  self.config.get('main', 'user')
      password =  self.config.get('main', 'password')
    except ConfigParser.Error:
      user = raw_input('Username: ')
      password = getpass.getpass('Password for user %s:'%user)

    cj = cookielib.CookieJar()
    cxt = ssl.create_default_context(cafile="ssl.pem")
    self.opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cj),
        urllib2.HTTPSHandler(debuglevel=0,context=cxt)
        )

    home = self.opener.open('https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort')

    tree = html.fromstring(home.read())
    form = tree.find('.//form')
    post = self.opener.open('https://login.1and1.org/ims-sso/login?service=http%3A%2F%2Ftimsato.tool.1and1.com%2Fxml%2Fenter%2Feffort',
        urlencode({"username": user,
          "password": password,
          "lt": form.find('.//input[@name="lt"]').value,
          "execution": form.find('.//input[@name="execution"]').value,
          "_eventId": form.find('.//input[@name="_eventId"]').value,
          "submit": form.find('.//input[@name="submit"]').value}))
    #print post.read()
    if post.geturl().startswith('https://login.1and1.org/'):
      if post.read().find('Invalid credentials'):
        raise Exception('Login failed')
      else:
        raise Exception('Forward to timsato failed')

    self.curday = date.today()
    self.url = post.geturl()


  def work(self, day, duration, project, task, comment=''):
    date_t = (day.day, day.month, day.year)

    #strange: if you book for past days you have to 'post' the __from for this day
    #to be able to book the first section
    if self.curday != day:
      #print 'curday ' + str(self.curday) + ' differs from ' + str(day) + ' post __from first'
      set_day = self.opener.open(self.url, urlencode({"__from": "%02d.%02d.%d" % date_t}))
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
    #print html_resp
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
        print 'SKIP: ' + section + ' - mandatory field "' + mandatory + '" missing'
        isok = False
    try:
      sect['comment'] = self.config.get(section, 'comment')
    except ConfigParser.Error:
      sect['comment'] = ''
    if isok:
      #print 'book section "' + section + '" with:'
      #self.printdictionary(sect)
      self.work(day, sect['duration'], sect['project'], sect['task'], sect['comment'])


  def workdaysfromconfig(self, begin, end):
    for o in range(begin.toordinal(), end.toordinal() + 1):
      day = date.fromordinal(o)
      if day.isoweekday() <= 5:
        print day
        self.bookfromconfig(day)


  def printdictionary(self, items):
    for key in items.keys():
      print ' ' + key + ': ' + items[key]


f = Filler()
#book single work-targets with:
#f.work(date.today(), '0:01', 'p.toh8.xxxxxxxxxxx', 'sa', 'auto')
#f.work(date(2015, 12, 27), '0:01', 'p.toh8.xxxxxxxxxxx', 'sa', 'auto')
#
#book single day from configfile:
f.bookfromconfig(date.today())
#f.bookfromconfig(date(2015, 12, 27))
#
#book range of workdays from configfile
#f.workdaysfromconfig(date(2015, 12, 23), date.today())
