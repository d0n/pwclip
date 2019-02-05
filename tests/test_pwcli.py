import sys
import unittest

from pwclip.cmdline import confpars, cli, gui, PassCrypt

class TestPWClip(unittest.TestCase):
	def test_pwcli(self):
		pwcli = PassCrypt()
		text = pwcli.lspw()
		self.assertIsNotNone(text, 'lspw broken')
		self.assertIs(type(text), dict, '%s breaks for not beeing of type dict '%text)




if __name__ == '__main__':
    unittest.main()
