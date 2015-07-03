import sys
from os.path import dirname as _dirname, abspath as _abspath, isdir as _isdir
__version__ = '1.2.5'
__dir__ = _dirname(_abspath(__file__))

if _isdir('%s/../../lib'%__dir__):
    __pydir__ = _abspath('%s/..'%__dir__)
    sys.path = [__pydir__] + [p for p in sys.path if p != __pydir__]


from misc import which, whoami

from .executor import Command
command = Command('sh_')
sucommand = Command('sh_', 'su_')
