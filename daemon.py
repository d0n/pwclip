#!/usr/bin/env python3
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
"""
daemonizing class - can be used as base class for any class to be daemonized
by just overriding the run method followed by executing the start method
what will cause the run method to be executed using the interval property
as timer
"""
# global & stdlib imports
import os
import sys
import time
import atexit

# default constant definitions
__version__ = '0.3'
__author__ = 'd0n@janeiskla.de'

class Daemon(object):
	"""daemon base class"""
	_dbg = False
	_pid = None
	_uid = int(os.getuid())
	_gid = int(os.getgid())
	_interval = 60 # seconds
	_umask = 0o022
	_stdin = open(os.devnull, 'r')
	_stdout = open(os.devnull, 'a+')
	_stderr = open(os.devnull, 'a+')
	__piddir = '/var/run'
	if os.getuid() != 0:
		__piddir = '%s/user/%s'%(__piddir, os.getuid())
	__me = os.path.basename(sys.argv[0])
	if '.' in __me:
		__me = __me.split('.')[0]
	_pidfile = '%s/%s.pid'%(__piddir, __me)
	def __init__(self, *args, **kwargs):
		"""
		initializing function which takes args and kwargs - init checks for
		args and kwars keys if it exsists in self and sets appropriate values
		each argument in args is considered a bool and sets the value to true
		"""
		for arg in args:
			arg = '_%s'%(arg)
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			key = '_%s'%(key)
			if hasattr(self, key):
				setattr(self, key, val)
		if self._dbg:
			print(Daemon.__mro__)
			for (key, val) in self.__dict__.items():
				print(key, '=', val)
	# rw properties
	@property #dbg <bool>
	def dbg(self):
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = val if type(val) is bool else self._dbg
	@property #uid <int>
	def uid(self):
		return self._uid
	@uid.setter
	def uid(self, val):
		self._uid = val if type(val) is int else self._uid
	@property #gid <int>
	def gid(self):
		return self._gid
	@gid.setter
	def gid(self, val):
		self._gid = val if type(val) is int else self._gid
	@property #interval <int>
	def interval(self):
		return int(self._interval)
	@interval.setter
	def interval(self, val):
		self._interval = val if val is int else self._interval
	@property #pidfile <str>
	def pidfile(self):
		return self._pidfile
	@pidfile.setter
	def pidfile(self, val):
		self._pidfile = val if val is str else self._pidfile
	# ro properties
	@property #umask
	def umask(self):
		return self._umask
	@property #stdin
	def stdin(self):
		return self._stdin
	@property #stdout
	def stdout(self):
		return self._stdout
	@property #stderr
	def stderr(self):
		return self._stderr
	@property # pid <int>
	def pid(self):
		if os.path.isfile(self.pidfile):
			with open(self.pidfile, 'r') as f:
				return int(f.read())

	def __rise(self):
		"""daemonize by double fork"""
		if self.dbg:
			print('1st fork...')
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError:
			sys.stderr.write('fork #1 failed')
			sys.exit(1)
		if self.uid != os.getuid():
			os.setuid(self.uid)
		if self.gid != os.getgid():
			os.setgid(self.gid)
		os.setsid()
		os.umask(self.umask)
		if self.dbg:
			print('2nd fork...')
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError:
			sys.stderr.write('fork #2 failed')
			sys.exit(1)
		with open(self.pidfile, 'w+') as f:
			f.write(str(os.getpid()).strip())
		if self.dbg:
			print("Started with pid %s"%(self.pid))
		sys.stdout.flush()
		sys.stderr.flush()
		os.dup2(self.stdin.fileno(), sys.stdin.fileno())
		os.dup2(self.stdout.fileno(), sys.stdout.fileno())
		os.dup2(self.stderr.fileno(), sys.stderr.fileno())
		atexit.register(self._delpid)

	def _delpid(self):
		"""delete the pidfile if it exists"""
		if os.path.exists(self.pidfile):
			os.remove(self.pidfile)

	def _running(self):
		"""double check if our pid exists within /proc"""
		if self.pid:
			if os.path.exists('/proc/%s'%(self.pid)):
				return True
			if self.dbg:
				print(
				    'Warning: %s: pidfile exists but %s could not be found ' \
				    'in /proc'%(self._running, self.pid), file=sys.stderr)

	def run(self):
		"""placeholder method which should be overridden"""
		pass

	def start(self):
		"""
		start function for running the run function every time the interval
		in seconds is reached
		"""
		if self._running():
			if self.dbg:
				print('already running with pid %i'%(self.pid))
			return
		if self.dbg:
			print('starting...')
		self.__rise()
		while True:
			self.run()
			time.sleep(self.interval)

	def stop(self, aggressor=15):
		"""
		while the pidfile exists we kill ourselfes
		first 3 times TERM(15) then KILL(9)
		"""
		if self.dbg:
			print('stopping...')
		pid = self.pid
		if not pid:
			self._delpid()
			if self.dbg:
				print('not running or pidfile removed')
			return
		aggressor = 15
		wait = 2
		i = 1
		while True:
			if self.dbg:
				times = 'th'
				if i == 1:
					times = 'st'
				elif i == 2:
					times = 'nd'
				print(
				    'trying to kill process with PID %s for the %i%s time ' \
				    'with signal %i waiting %isec bevore retrying'%(
				        pid, i, times, aggressor, wait)
				    )
			if i >= 3:
				aggressor = 9
				wait = 0.5
			try:
				os.kill(pid, aggressor)
			except ProcessLookupError:
				self._delpid()
				break
			except PermissionError:
				print('no permissions to kill process with PID %s'%(pid))
				return False
			try:
				os.kill(pid, 0)
			except ProcessLookupError:
				if self.dbg:
					print('stopped')
				return True
			time.sleep(wait)
			i += 1

	def restart(self):
		self.stop()
		self.start()

	def status(self):
		if self.pid and os.path.isdir('/proc/%s'%(self.pid)):
			with open('/proc/%s/status'%(self.pid), 'r') as stf:
				return stf.read()
		elif self.pid:
			if self.dbg:
				print('%s PID %s could not be found in /proc - pidfile %s ' \
				    'will be deleted'%(self.status, self.pid, self.pidfile))
			self._delpid()
		else:
			if self.dbg:
				print('currently not running (no pidfile %s)'%(self.pidfile))
		return False








if __name__ == '__main__':
	# example of daemon usage without class invokation
	# create the daemon instance
	#daemon = Daemon(*('dbg', ), **{'interval':3600})
	# just a function to be executed
	def write_stamp():
		import datetime as dt
		with open('/tmp/daemon.txt', 'w+') as f:
			now = dt.datetime.now()
			f.write(str(now.date())+'.'+str(now.time()).split('.')[0])
	# overriding run method with that function
	#daemon.run = write_stamp

	# OR

	# example usage by invoking the daemon class
	class TestDaemon(Daemon):
		# overriding run method
		def run(self):
			write_stamp()
	#daemon = TestDaemon(*('dbg', ), **{'interval':3600})
	daemon = TestDaemon()

	# and finally simply execute the start or stop action
	if len(sys.argv) > 1:
		if sys.argv[1] == 'start':
			# start the daemon
			daemon.start()
		elif sys.argv[1] == 'stop':
			# stop the daemon
			daemon.stop()
		elif sys.argv[1] == 'status':
			# stop the daemon
			daemon.status()
