__version__ = '0.1'
from .crontools import stamp, fileage
from .misctools import which, random, string2bool
from .pathtools import bestlim, lineno, realpaths, confpaths, confdats
from .users import Users

user = Users()
