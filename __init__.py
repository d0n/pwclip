__version__ = '0.1'

from .cronologic import stamp, fileage

from .path import absrelpath, realpaths, confpaths, confdats, jconfdats

from .blockdevice import BlockDevice

from .sysfs import SysFs

from .bestlim import bestlim

from .lineno import lineno

from .which import which

from .random import random

from .string2bool import string2bool

from .hostname import hostname

from .gpgagent import agentinfo

from .user.whoami import whoami
from .user.find import userfind
