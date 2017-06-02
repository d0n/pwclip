#!/usr/bin/env python3
#
# This file is free software by  <- d0n - d0n@janeiskla.de ->
#
# You can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY! Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# Write to the Free Software Foundation, Inc.
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
# global imports
from threading import Thread, Lock
from queue import Queue


def parfuniter(iterates, function, threads=3, **args):
	"""parallel function iterator"""
	lock = Lock()
	queue = Queue()

	def _worker(**args):
		while True:
			item = queue.get()
			function(**args)
			queue.task_done()

	for i in range(threads):
		trd = Thread(target=_worker, args=(**args))
		trd.daemon = True
		trd.start()
	for trg in iterates:
		queue.put
