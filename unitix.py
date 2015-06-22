#!/usr/bin/env /usr/bin/python3
#
# This file is free software by d0n <d0n@janeiskla.de>
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

# local relative imports
from executor import Command
from colortext import blu, red, yel, byel, error, fatal

# global default variables
__version__ = '0.0'

class UnitixUsers(Command):
	sh_ = True
	acclog = 'acclog.server.lan'
	login = 'lpelzer'
	def _chkuser(self, user):
		def __hasaccount(user):
			passwd = self.stdx(
			    'cat /etc/passwd', host=self.acclog, user=self.login)
			for line in passwd.split('\n'):
				if line.split(':')[0].strip() == user:
					return True
		def __clusters(user):
			groups = self.stdx(
				'cat /etc/group', host=self.acclog, user=self.login)
			clusters = []
			for line in groups.split('\n'):
				if user in line:
					clusters.append(line.split(':')[0])
			return clusters
		if __hasaccount(user):
			return {user:__clusters(user)}

	def _adduser(self, user, groups):
		usergroups = self._chkuser(user)
		if usergroups:
			groups = [g for g in groups if not g in usergroups[user]]
			for group in groups:
				out, err, rtc = self.oerc(
					'adduser', user, group, host=self.acclog, user='root')
				if rtc != 0:
					error(
						'while adding user', user, 'to group',
						group, 'the following error occoured:\n', err
						)
			message = '%s %s %s\n%s\n'%(
				blu('successfully added user'), yel(user),
				blu('to group(s):'), '\n'.join(byel(g) for g in groups))
		else:
			message = message = '%s %s %s'%(
			    blu('user'), yel(user), blu('does not exist'))
		return message

	def _deluser(self, user, groups):
		usergroups = self._chkuser(user)
		if usergroups:
			grps = [g for g in groups if g in usergroups[user]]
			if grps:
				for group in grps:
					out, err, rtc = self.oerc(
						'deluser', user, group, host=self.acclog, user='root')
					if rtc != 0:
						error(
							'while deleting user', user, 'from group',
							group, 'the following error occoured:\n', err
							)
				message = '%s %s %s\n%s\n'%(
					blu('successfully deleted user'), yel(user),
					blu('from group(s):'), '\n'.join(byel(g) for g in grps))
			else:
				message = '%s %s %s %s'%(
				    red('user'), yel(user),
				    red('isn\'t member of group'),
				    yel(' '.join(g for g in groups)))
		else:
			message = '%s %s %s'%(
			    red('user'), yel(user), red('does not exist'))
		return message


	def users(self, *users, groups=None, mode=None):
		message = ''
		if mode:
			if mode == 'add':
				for user in users:
					message = '%s%s'%(message, self._adduser(user, groups))
			elif mode == 'del':
				for user in users:
					message = '%s%s'%(message, self._deluser(user, groups))
		else:
			for user in users:
				usergroups = self._chkuser(user)
				if usergroups:
					msg = '%s %s %s'%(
						blu('The user'), yel(user), blu('has an UNITIX account'))
					if usergroups[user] != []:
						msg = '%s %s\n%s\n'%(msg, blu('and is a member of the\n' \
							'following cluster group(s):'), '\n'.join(
							byel(g) for g in usergroups[user]))
					else:
						msg = '%s %s'%(
							msg, blu('but isn\'t member of any group.\n'))
				else:
					msg = '%s %s %s'%(
						red('The user'), yel(user),
						red('has no UNITIX account!\n'))
				message = '%s%s'%(message, msg)
		return message









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
