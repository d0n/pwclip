#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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
"""parafun main program"""
from colortext import tabd
from threading import Lock, Thread, current_thread
from queue import Queue

__version__ = '0.1'

def parafun(function, iterable, procnum=None, *args, **kwargs):
	global _lock
	_lock = Lock()
	queue = Queue()
	procnum = procnum if procnum else len(iterable)
	def _iterqueue(function, args, **kwargs):
		while True:
			item = queue.get()
			if item is None:
				break
			if args and kwargs:
				function(item, *args, **kwargs)
			elif args:
				function(item, *args)
			elif kwargs:
				function(item, **kwargs)
			else:
				function(item)
			queue.task_done()
	threads = []
	try:
		for i in range(procnum):
			print(tabd(dict(Thread.__dict__)))
			trd = Thread(
                target=_iterqueue, args=(function, args), kwargs=kwargs)
			exit()
			trd.daemon = True
			trd.start()
			threads.append(trd)
		for item in iterable:
			queue.put(item)
	except KeyboardInterrupt:
		exit(1)
	finally:
		for i in range(procnum):
			queue.put(None)
	for t in threads:
		try:
			t.join()
		except:
			break
