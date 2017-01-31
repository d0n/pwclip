# -*- coding: utf-8 -*-
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""python3 daemon"""
# (std)lib imports
from os import \
    getuid, setuid, getgid, \
    setgid, getpid, devnull, \
    fork, kill, umask, remove, \
    setsid, dup2, nice

from os.path import \
    basename, isfile, exists, isdir

from sys import \
    argv, stdin, stdout, stderr

from atexit import register

from time import sleep

_echo_ = stdout.write
_puke_ = stderr.write

class Daemon(object):
	"""
	daemonizing class - can be used as base class for any class to be
	daemonized by just overriding the run method followed by executing the
	start method what will cause the run method to be executed using the
	interval property as timer
	"""
	dbg = False
	pid = None
	uid = int(getuid())
	gid = int(getgid())
	interval = 60 # seconds
	umask = 0o022
	stdin = open(devnull, 'r')
	stdout = open(devnull, 'a+')
	stderr = open(devnull, 'a+')
	__me = basename(argv[0]).split('.')[0]
	_pidfile = '/var/run/%s.pid'%__me
	if getuid() != 0:
		_pidfile = '/var/run/user/%s/%s.pid'%(getuid(), __me)
	def __init__(self, *args, **kwargs):
		"""
		initializing function which takes args and kwargs - init checks for
		args and kwars keys if it exsists in self and sets appropriate values
		each argument in args is considered a bool and sets the value to true
		"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			_echo_('\033[01;30%s\033[0m'%sDaemon.__mro__)
			_echo_('\033[01;30%s\033[0m'%sDaemon.__dict__)
			_echo_('\033[01;30%s\033[0m'%self.__init__)
			_echo_('\033[01;30%s\033[0m'%self.__dict__)

	@property               # pidfile <str>
	def pidfile(self):
		return self._pidfile
	@pidfile.setter
	def pidfile(self, val):
		val = '%s.pid'%val if not val.endswith('pid') else val
		if not val.startswith('/'):
			__piddir = '/var/run'
			if getuid() != 0:
				__piddir = '%s/user/%s'%(__piddir, getuid())
			val = '%s/%s'%(__piddir, val)
		self._pidfile = val

	@property # pid <int>
	def pid(self):
		"""pid getter"""
		if _isfile(self.pidfile):
			with open(self.pidfile, 'r') as pidf:
				pid = pidf.read().strip()
			if pid:
				return int(pid)

	def _rise(self):
		"""daemonize by double fork"""
		if self.dbg:
			_echo_('\033[01;30m1st fork...\033[0m\n')
		try:
			pid = _fork()
			if pid > 0:
				exit(0)
		except OSError:
			_puke_('fork #1 failed\n')
			exit(1)
		if self.dbg:
			_echo_('\033[01;30m2nd fork...\033[0m\n')
		try:
			pid = _fork()
			if pid > 0:
				exit(0)
		except OSError:
			_puke_('fork #2 failed\n')
			exit(1)
		if self.uid != _getuid():
			_setuid(self.uid)
		if self.gid != _getgid():
			_setgid(self.gid)
		_setsid()
		_umask(self.umask)
		try:
			_nice(int(self.nice))
		except OSError:
			if self.dbg:
				_puke_('\033[01;30mcould not set ' \
                    'process niceness to %i\033[0m\n'%(self.nice))
		with open(self.pidfile, 'w+') as pidf:
			pidf.write(str(_getpid()).strip())
		if self.dbg:
			_echo_('\033[01;30mdaemonized pid %s\033[0m\n'%self.pid)
		_stdout.flush()
		_stderr.flush()
		_dup2(self.stdin.fileno(), _stdin.fileno())
		# dont redirect stdout/stderr if debugging
		if not self.dbg:
			_dup2(self.stdout.fileno(), _stdout.fileno())
			_dup2(self.stderr.fileno(), _stderr.fileno())
		_register(self._delpid)

	def _delpid(self):
		"""delete the pidfile if it exists"""
		if _exists(self.pidfile):
			_remove(self.pidfile)

	def _running(self):
		"""double check if our pid exists within /proc"""
		if self.pid:
			if _exists('/proc/%s'%(self.pid)):
				return True
			if self.dbg:
				_stderr.write(
                    '\033[01;30mWarning: %s: pidfile exists but %s could ' \
                    'not be found in /proc\033[0m\n'%(self._running, self.pid))
	def run(self):
		"""placeholder method which should be overridden"""
		pass

	def start(self):
		"""
		start function for running the run function every time the interval
		in seconds is reached
		"""
		if self._running():
			if not self.dbg: return
			_echo_('\033[01;30malready running with pid %i\033[0m\n'%self.pid)
		if self.dbg: _echo_('\033[01;30mstarting...\033[0m\n')
		self._rise()
		while True:
			self.run()
			_sleep(self.interval)

	def stop(self, aggressor=15):
		"""
		while the pidfile exists we kill ourselfes
		first 3 times TERM(15) then KILL(9)
		"""
		if self.dbg:
			_echo_('\033[01;30mstopping...\033[0m\n')
		pid = self.pid
		if not pid:
			self._delpid()
			if self.dbg:
				_echo_('\033[01;30mnot running or pidfile removed\033[0m\n')
			return
		wait = 2.0
		i = 0
		while True:
			if self.dbg:
				times = 'th'
				if i == 1: times = 'st'
				elif i == 2: times = 'nd'
				_echo_(
                    '\033[01;30mtrying to kill process with PID %s '
                    'for the %i%s time with signal %i waiting %isec '
                    'bevore retrying\033[0m\n'%(pid, i+1, times, aggressor, wait))
			if i >= 3:
				aggressor = 9
				wait = 0.1
			try:
				_kill(pid, aggressor)
			except ProcessLookupError:
				self._delpid()
			except PermissionError:
				_stderr.write(
                    'no permissions to kill process with PID %s\n'%pid)
			else:
				self._delpid()
				break
			_sleep(wait)
			i += 1
		return True

	def restart(self):
		"""just trigger stop and start"""
		self.stop()
		self.start()

	def status(self):
		"""
		return the deamons current status:
		pid if its running
		bool(False) if its not running
		"""
		if self.pid and _isdir('/proc/%s'%(self.pid)):
			with open('/proc/%s/status'%(self.pid), 'r') as stf:
				return stf.read()
		elif self.pid:
			if self.dbg:
				_echo_('\033[01;30m%s PID %s could not be found in /proc ' \
                    '- pidfile %s will be deleted\033[0m\n'%(
                        self.status, self.pid, self.pidfile))
			self._delpid()
		else:
			if self.dbg:
				_echo_('\033[01;30mcurrently ' \
				    'not running (no pidfile %s)\033[0m\n'%(self.pidfile))
		return False








if __name__ == '__main__':
	# example of daemon usage without class invokation
	# create the daemon instance
	#daemon = Daemon(*('dbg', ), **{'interval':3600})
	# just a function to be executed
	#def write_stamp():
	#	import datetime as dt
	#	with open('/tmp/daemon.txt', 'w+') as f:
	#		now = dt.datetime.now()
	#		f.write(str(now.date())+'.'+str(now.time()).split('.')[0])
	# overriding run method with that function
	#daemon.run = write_stamp
    #
	# OR
    #
	# example usage by invoking the daemon class
   	#class TestDaemon(Daemon):
	#	# overriding run method
	#	def run(self):
	#		write_stamp()
	#daemon = TestDaemon(*('dbg', ), **{'interval':3600})
	#daemon = TestDaemon()
    #
	# and finally simply execute the start or stop action
	#if len(sys.argv) > 1:
	#	if sys.argv[1] == 'start':
	#		# start the daemon
	#		daemon.start()
	#	elif sys.argv[1] == 'stop':
	#		# stop the daemon
	#		daemon.stop()
	#	elif sys.argv[1] == 'status':
	#		# get status of daemon
	#		daemon.status()
	print('\n'.join(m for m in dir()))
