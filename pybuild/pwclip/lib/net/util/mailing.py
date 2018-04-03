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
"""mailing module disclaimer"""
# global & stdlib imports
from smtplib import SMTP
from email.mime.text import MIMEText
from getpass import getpass

from colortext import error


def sendmail(message, sender, sendto, subject='',
      server='smtp.1und1.de', smtpuser=None, smtppass=None):
	"""sndmail to provide function"""
	if not sender or not sendto:
		return error('cannot sent mail if sender and recipient is not set')
	smtppass = getpass() if smtpuser else None
	msg = MIMEText(message)
	if subject:
		msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = sendto
	smtp = SMTP(server)
	if smtpuser and smtppass:
		smtp.login(smtpuser, smtppass)
	smtp.sendmail(sender, sendto, msg.as_string())
	smtp.quit()






if __name__ == '__main__':
	#
	# module debugging area
	#
	#print('\n'.join(d for d in dir()))
	exit(1)
