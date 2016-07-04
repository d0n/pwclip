"""clipboard handler"""
from subprocess import Popen, DEVNULL, PIPE

from colortext import fatal

from .which import which

xsel = which('xsel')
def clipper(data, board='b', mode=None):
	mode = mode if mode else '-o'
	mode = '-i' if data else '-o'
	cmds = [xsel, mode, '-%s'%board]
	if data:
		p = Popen(cmds, stdin=PIPE)
		p.communicate(input=data.encode('utf-8'))
		cmds = [xsel, '-o', '-%s'%board]
	p = Popen(cmds, stdout=PIPE)
	out, _ = p.communicate()
	return out.decode()


class ClipBoard(object):
	_dbg = False
	_xsel = which('xsel')
	# -i --input | -o --output
	_mode = '--output'
	# -p --primary | -s --secondary | -b --clipboard
	_board = '--clipboard'
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in ClipBoard.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                ClipBoard.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(ClipBoard.__dict__.items())),
                ClipBoard.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = True if val else False

	@property                # mode <str>
	def mode(self):
		return self._mode
	@mode.setter
	def mode(self, val):
		assert val in ('i', 'input', 'o', 'output')
		self._mode = '--%s'%val
		if len(val) == 1:
			self._mode = '-%s'%val

	@property                # board <str>
	def board(self):
		return self._board
	@board.setter
	def board(self, val):
		assert val in (
            'p', 'primary',
            's', 'secondary',
            'b', 'clipboard'
            'x', 'exchange')
		self._board = '--%s'%val
		if len(val) == 1:
			self._board = '-%s'%val

	@property                # xsel <str>
	def xsel(self):
		if not self._xsel:
			error('the program', 'xsel', 'is missing')
		return self._xsel

	def clip(self, data=None):
		p = Popen([self.xsel, self.mode, self.board])
		if data:
			p.communicate(input=data.encode('utf-8'))
			p = Popen([self.xsel, self.mode, self.board])
		out, _ = p.communicate()
		if out:
			return out.decode()
