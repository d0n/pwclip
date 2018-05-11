import sys
from unittest import TestCase
from pwclip.cmdline import argspars, confargs, cli

class CommandLineTestCase(TestCase):
	"""
	Base TestCase class, sets up a CLI parser
	"""
	@classmethod
	def setUpClass(cls):
		cls.parser = argspars('cli')
		cls.args, cls.pargs, cls.pkwargs = cls.parser


class TestCase4pwcli(CommandLineTestCase):
	def test_with_empty_args():
		"""
		User passes no args, should fail with SystemExit
		"""
		with self.assertRaises(SystemExit):
			self.parser.parse_args([])

	def test_list_entrys():
		"""
		Find database servers with the Ubuntu AMI in Australia region
		"""
		cli(confsargs())
