#!/usr/bin/env /usr/bin/python3
#
# This file is free software by  <- d0n - d0n@janeiskla.de ->
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""module disclaimer"""

# global & stdlib imports
#import re
import os
import sys
import ldap3

# local relative imports
from colortext import blu, yel, bgre, error

# global default variables
__version__ = '0.0'

"""
# 21232445, People, contacts, 1und1, DE
dn: uid=21232445,ou=People,ou=contacts,o=1und1,c=DE
cn: Pelzer, Leon
preferredLanguage: de_DE
mail: leon.pelzer@1und1.de
displayName: Pelzer, Leon
initials: LP4
uid: 21232445
telephoneNumber: +49 721 91374-3510
sn: Pelzer
givenName: Leon
o: lpelzer
postalAddress: Karlsruhe-Brauerstrasse 48
employeeType: employee
ou: IT Operations Access Middleware
departmentNumber: 21424185
labeledURI: http://intranet.1and1.com/people/21232445
objectClass: person
objectClass: inetOrgPerson
objectClass: uidObject
"""

class LDAPSearch(object):
	_dbg = None
	_con = None
	_server = 'ldap.1and1.org'
	_basedn = 'ou=contacts,o=1und1,c=DE'
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not type(val) in (None, bool):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(LDAPSearch.__mro__))
			print(bgre(tabd(self.__dict__, 2)))

	@property               # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property               # con <bool>
	def con(self):
		return self._con
	@con.setter
	def con(self, val):
		self._con = val if type(val) is bool else self._con
	@property               # basedn <str>
	def basedn(self):
		return self._basedn
	@basedn.setter
	def basedn(self, val):
		self._basedn = val if type(val) is str else self._basedn
	@property               # server <str>
	def server(self):
		return self._server
	@server.setter
	def server(self, val):
		self._server = val if type(val) is str else self._server

	def __connect(self):
		if self.dbg:
			print(bgre(self.__connect))
		if not self.con:
			self.ldap = ldap3.Connection(
                ldap3.Server(self.server, get_info=ldap3.GET_ALL_INFO),
                auto_bind=True)
			self.con = True

	def _translator(self, data):
		if self.dbg:
			print(bgre(self._translator))
		dictionary={
            'displayName':'name', 'telephoneNumber':'telephone',
            'ou':'department', 'postalAddress':'address', 'mail':'e-mail',
            'labeledURI':'profile', 'o':'Shortcut'}
		filtereds = {}
		for (typ, atr) in sorted(data.items()):
			for (key, val) in sorted(dictionary.items()):
				if typ == key:
					filtereds[val] = atr[0].decode()
		return filtereds

	def _seek(self, pattern, typ):
		if self.dbg:
			print(bgre(self._seek))
		self.__connect()
		response = []
		if self.ldap.search(
              self.basedn, '(%s=%s)'%(typ, pattern),
              ldap3.SEARCH_SCOPE_WHOLE_SUBTREE, attributes=['*']):
			return self.ldap.response

	def _result(self, results):
		if self.dbg:
			print(bgre(self._result))
		msgs = []
		if results:
			msg = ''
			for attr in sorted(results):
				if attr:
					Attr = '%s%s'%(attr[0].upper(), attr[1:])
				if '-' in Attr:
					Attr = '%s-%s%s'%(
                        attr[0].upper(),
                        attr.split('-')[1][0].upper(),
                        attr.split('-')[1][1:])
				lim = 15-len(Attr)
				msg = '%s\n  %s%s%s'%(
                    msg, blu(Attr), ' '*lim, yel(str(results[attr])))
		return '  %s'%msg.strip()

	def seek1and1(self, *patterns, mode=None):
		if self.dbg:
			print(bgre(self.seek1and1))
		if mode is None:
			mode = 'ins'
		if mode == 'tmn':
			typ = 'cn'
			pattern = ' '.join(p for p in patterns)
			pattern = 'Dep_%s'%(pattern.strip())
			results = self._seek(pattern, typ)
			if results and len(results) == 1:
				headuid = results[0]['attributes']['headof'][0]
				teamname = pattern[4:]
				linelen = 55
				trench = '%s'%('-'*int(int(linelen-len(teamname))/2))
				msg = ' %s Head of %s %s'%(trench, teamname, trench)
				print(msg)
				pattern = headuid.split('=')[1]
				typ = 'uid'
				results = self._seek(pattern, typ)
				print(self._result(
                    self._translator(results[0]['raw_attributes'])))
				print(' %s\n %s'%('-'*65, '-'*65))
			typ = 'ou'
			pattern = ' '.join(p for p in patterns)
			pattern = pattern.strip()
			results = self._seek(pattern, typ)
			if results:
				for result in results:
					print(self._result(
                        self._translator(result['raw_attributes'])), '\n')
			else:
				error('ldap search returned no hits for', pattern)
		elif mode == 'fun':
			typ = 'cn'
			if len(patterns) < 2:
				fatal(
                    'full name must at least consist ' \
                    'of a forename and surname')
			forename = patterns[0]
			surnames = patterns[1:]
			if not forename[0].isupper():
				forename = '%s%s'%(
                    forename[0].upper(),
                    ''.join(n for n in forename[1:]))
			lastnames = []
			for surname in surnames:
				if len(surname) < 3:
					lastnames.append(surname)
				elif not surname[0].isupper():
					lastnames.append(
                        '%s%s'%(surname[0].upper(),
                        ''.join(n for n in surname[1:])))
				else:
					lastnames.append(surname)
			if len(lastnames) == 1:
				fullname = '%s, %s'%(lastnames[0], forename)
			else:
				fullname = '%s, %s'%(
                    ' '.join(n for n in lastnames), forename)
			fullname = fullname.strip()
			results = self._seek(fullname, typ)
			if results:
				print(self._result(
                    self._translator(results[0]['raw_attributes'])))
			else:
				error(
                    'ldap search returned no hits for',
                    ' '.join(p for p in patterns))
		elif mode == 'ins':
			typ = 'o'
			for pattern in patterns:
				results = self._seek(pattern, typ)
				if results:
					print(self._result(
                        self._translator(
                            results[0]['raw_attributes'])), '\n'
                        )
				else:
					error('ldap search returned no hits for', pattern)
		else:
			error('unknown mode', mode)















if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	#ldap = LDAPSearch('dbg')
