# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.

class Debugger(object):
	_dbg = False
	_vrb = False
	_logfile = ''
	def __init__(self):
		pass
		if self.dbg:
			lim = int(max(len(k) for k in Debugger.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                Debugger.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(Debugger.__dict__.items())),
                Debugger.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(
                    int(max(len(i) for i in self.__dict__.keys())+4
                    )-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False
	@property                # vrb <bool>
	def vrb(self):
		return self._vrb
	@vrb.setter
	def vrb(self, val):
		self._vrb = True if val else False
	@property                # logfile <str>
	def logfile(self):
		return self._logfile
	@logfile.setter
	def logfile(self, val):
		self._logfile = val if not val.startswith('~') else _expanduser(val)
		if not _isdir(_dirname(val)):
			raise FileNotFoundError(
                '"%s" no such file or directory'%_dirname(val))
	def debug(self, message='', debug=None, verbose=None):
		dbg = debug if debug is not None else self.dbg
		vrb = verbose if verbose is not None else self.vrb
		if dbg:
			__stack = '%s: %s'%(_stack()[-1][1], str(_stack()[2]).strip('()'))
			if message:
				message = message if not vrb else '%s << %s >>'%(
                    __stack, message)
			message = __stack if not message else message
			if self.logfile:
