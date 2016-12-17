#!/usr/bin/env python3
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
from time import sleep
from getpass import getpass

# local relative imports
from lib.network import sendmail
from lib.system import which, confdats
from lib.executor import command
from modules.colortext import blu, grn, yel, 

# global default variables
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.path.abspath(os.readlink(os.path.dirname(__file__)))
__version__ = '0.0'


def fromtosub():
	print(grn('enter the'), yel('e-mail-address'),
        grn('you want to send from'))
	sender = input()
	print(grn('enter the'), yel('e-mail-address'),
        grn('you want to send to'))
	sendto = input()
	print(grn('enter a'), yel('subject'),
        grn('for the message'))
	subject = input()
	return sender, sendto, subject

def mailer():
	import argparse
	cfgfile = '%s/config/%s.conf'%(__at__, __me__)
	msgfile = os.path.expanduser('~/tmp/msg')
	cfgs = confdats(cfgfile)
	egf = 'e.g. foo@bar.com'
	egs = 'e.g. foo@bar.com'
	if type(cfgs) is dict and 'user' in cfgs.keys():
		if 'sender' in cfgs['user'].keys():
			egf = 'is %s'%cfgs['user']['sender']
			sender = cfgs['user']['sender']
		if 'sendto' in cfgs['user'].keys():
			egs = 'is %s'%cfgs['user']['sendto']
			sendto = cfgs['user']['sendto']

	__dsc__ = '%s <by d0n@janeiskla.de> DESCRIPTION'%(__me__)
	parser = argparse.ArgumentParser(description=__dsc__)
	parser.add_argument(
	    '--debug',
	    dest='dbg', action='store_true',
	    help='enable debugging output')
	parser.add_argument(
	    '--verbose',
	    dest='vrb', action='store_true',
	    help='enable jabbering mode')
	parser.add_argument(
	    '--version',
	    action='version', version='%s v%s'%(__me__, __version__))
	userg = parser.add_argument_group('user')
	userg.add_argument(
	    '-f',
	    dest='sender', metavar='MAILADDR',
	    help='set the sender address to MAILADDR (%s)'%egf)
	userg.add_argument(
	    '-t',
	    dest='sendto', metavar='MAILADDR',
	    help='set the recipient address to MAILADDR (%s)'%egs)
	userg.add_argument(
	    '-F',
	    dest='msgfile', metavar='MSGFILE',
	    help='set the file containing the message (defaults to %s)'%msgfile)
	args = parser.parse_args()
	if not [v for v in args.__dict__.values() if v]:
		print('%s %s%s'%(blu('using'), yel(__me__),
		    blu('\'s interactive mode for sending mail')))
		sender, sendto, subject = fromtosub()
		if not sender:
			if 'user' in cfgs.keys() and 'sender' in cfgs['user'].keys():
				sender = cfgs['user']['sender']
		if not sendto:
			if 'user' in cfgs.keys() and 'sendto' in cfgs['user'].keys():
				sender = cfgs['user']['sendto']
		print(blu(
		    'now dropping you to your'), '$EDITOR', blu('to write your mail'))
		sleep(2)
		while True:
			command.call('%s %s'%(which(os.environ['EDITOR']), msgfile))
			print(grn('are you finished writing the mail?'), '[Y/n]')
			yesno = input()
			if yesno.lower() in ('y', ''):
				message = open(msgfile, 'r').read()
				break
		if not cfgs or not 'server' in cfgs.keys():
			print(grn('enter the'), yel('smtp-server'),
			    grn('which shall be used for sending'))
			smtp = input()
		smtp = cfgs['server']['smtp']
		user = os.getlogin()
		pwd = ''
		if 'user' in cfgs['server'].keys():
			user = cfgs['server']['user']
		else:
			print(grn('enter the user name for smtp-server authentication'))
			pwd = getpass()
		if 'pass' in cfgs['server'].keys():
			pwd = cfgs['server']['pass']
		else:
			print(
			    grn('enter the password for the user'), yel(user),
			    grn('for smtp-server authentication'))
			pwd = getpass()
		print(blu('the following mail will be sent')+':')
		msg = '[server]\n' \
		    'smtp    = {smtp}\n\n' \
		    '[user]\n' \
		    'from    = {sender}\n' \
		    'to      = {sendto}\n\n' \
		    '[mail]\n' \
		    'subject = {subject}\n' \
		    'message = ---\n{message}---\n'
		print(
		    msg.format(**{
		        'smtp':smtp, 'sender':sender,
		        'sendto':sendto, 'subject':subject, 'message':message})
		    )
		print(grn('can the message be sent?'), '[Y/n]')
		yesno = input()
		if yesno.lower() in ('y', ''):
			sendmail(
			    sender, sendto, message,
			    smtp, subject, smtpuser=user, smtppass=pwd)


	#if os.path.isfile(cfgs['mail']['message']):
	#	with open(
	#	message = 
	#print('\n'.join(m for m in message.split('\\n')))
	#print(msgcfgs['mail'])
