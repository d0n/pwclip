from os import kill

from time import sleep

from colortext import blu, yel, error

from executor import command

from net import ping

def jump(jumpcmd):
	trg = list(jumpcmd.split())[-1]
	if not ping(trg):
		error('target ', trg, ' does not respond to ping')
	pid = command.run(jumpcmd)
	print(blu('started process with PID'), yel(pid), flush=True)
	sleep(1.5)
	try:
		kill(pid, 0)
	except ProcessLookupError:
		error('process ', pid, ' died too soon after startup')

