#!/usr/bin/env python3

import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler

def logger(name, lvl='info'):
	# 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
	lvls = {
      'debug': logging.DEBUG,
      'info': logging.INFO,
      'warning': logging.WARNING,
      'error': logging.ERROR,
      'critical': logging.CRITICAL}
	_logger = logging.getLogger(name)
	_logger.setLevel(lvl if lvl in lvls.values() else lvls[lvl])
	formats = logging.Formatter("%(message)s")  # same as default
	handler = logging.FileHandler(name)
	handler.setFormatter(formats)
	_logger.addHandler(handler)
	return _logger
