import sys
from os.path import dirname as _dirname, abspath as _abspath, \
    isdir as _isdir, basename as _basename

__miscdir__ = _abspath('%s/..'%_dirname(__file__))
if _isdir(__miscdir__):
	sys.path = [__miscdir__] + [p for p in sys.path if p != __miscdir__]

from .executor import Command
from .sexecutor import SSHCommand
command = Command('sh')
sucommand = Command('sh', 'su')
