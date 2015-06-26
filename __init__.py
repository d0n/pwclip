__version__ = '1.2.5'

from lib import which, whoami

from .executor import Command
command = Command('sh_')
sucommand = Command('sh_', 'su_')
