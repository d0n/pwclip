"""clipboard handler"""
from subprocess import Popen, DEVNULL, PIPE

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from colortext import bgre, fatal, error

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
	_board = '--clipboard'
	#_xsel = which('xsel')
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

	@property                # board <str>
	def board(self):
		return self._board
	@board.setter
	def board(self, val):
		assert val in (
            'p', 'primary',
            's', 'secondary',
            'b', 'clipboard')
		self._board = '--%s'%val
		if len(val) == 1:
			self._board = '-%s'%val
	"""
	@property                # xsel <str>
	def xsel(self):
		if not self._xsel:
			error('the program', 'xsel', 'is missing')
		return self._xsel

	def copy(self, data):
		if self.dbg:
			print(bgre('%s\n  %s'%(self.copy, data)))
		Popen([self.xsel, '-i', self.board], stdin=PIPE).communicate(
            input=data.encode('utf-8'))

	#	def clipswitch(self, board):
	#		if board in (''

	def paste(self):
		if self.dbg:
			print(bgre(self.paste))
		out, _ = Popen(
            [self.xsel, '-o', self.board], stdout=PIPE).communicate()
		return out.decode()
	"""
	def clipper(self, data=None, board=None, mode=None, secure=False):
		mode = 'i' if data and mode == 'o' else mode
		mode = 'o' if not data and mode == 'i' else mode
		mode = mode if mode else 'o'
		self.board = board
		if self.dbg:
			print(bgre('%s\n  data=%s, board=%s, mode=%s'%(
                self.clipper, data, self.board, mode)))
		clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		clip.set_text('clitboard', -1)
		clip.store()
		print(Gtk.Clipboard.wait_for_contents())
		print(clip.wait_for_text())
		"""
		if secure:
			predata = self.paste()
		if mode == 'x':
			Popen([self.xsel, '-x']).communicate()
		if data:
			self.copy(data)
		try:
			return self.paste()
		finally:
			if secure:
				Popen([self.xsel, '-c', self.board]).communicate()
				self.copy(predata)
		"""
