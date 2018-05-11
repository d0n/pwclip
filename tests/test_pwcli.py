from unittest import TestCase
from pwclip.cmdline import cli, confpars

class CommandLineTestCase(TestCase):
	"""
	Base TestCase class, sets up a CLI parser
	"""
	@classmethod
	def setUpClass(cls):
		cls.args, cls.pargs, cls.pkwargs = confpars('cli')


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
		args = self.parser.parse_args(['pwcli', '-l'])
		result = cli(args.tags, args.region, args.ami)
		self.assertIsNotNone(result)
