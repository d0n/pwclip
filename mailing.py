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
from smtplib import SMTP as _smtp
from email.mime.text import MIMEText as _mimetext
from getpass import getpass as _getpass

# default constant definitions
__version__ = '0.1'

def sendmail(message, sender, sendto, subject='',
      server='smtp.1und1.de', smtpuser=None, smtppass=None):
	"""sndmail to provide function"""
	msg = _mimetext(message)
	if subject:
		msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = sendto
	smtp = _smtp(server)
	if smtpuser:
		smtp.login(smtpuser, smtppass)
	smtp.sendmail(sender, sendto, msg.as_string())
	smtp.quit()






if __name__ == '__main__':
	#
	# module debugging area
	#
	#print('\n'.join(d for d in dir()))
	exit(1)
