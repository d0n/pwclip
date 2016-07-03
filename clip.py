"""clipboard handler"""
from subprocess import Popen, DEVNULL, PIPE

from colortext import fatal

from .which import which

xsel = which('xsel')
def clipper(data, board='b', mode=None):
	mode = mode if mode else '-o'
	mode = '-i' if data else '-o'
	cmds = [xsel, mode, '-%s'%board]
	print(cmds)
	if not data:
		p = Popen(cmds, stdout=PIPE)
		out, _ = p.communicate()
		return out.decode()
	p = Popen(cmds, stdin=PIPE)
	p.communicate(input=data.encode('utf-8'))
