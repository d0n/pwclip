#!/usr/bin/env python3
"""discaimer"""
#global imports
import os
import sys
from xml.etree import ElementTree as ET
#local relative imports

#default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))
__version__ = '0.0'

# scheme: <sectors> <elements> <keys: values>


class JBossXML(object):
	_file = None
	_root = None
	def __init__(self, xmlfile):
		self._file = xmlfile
		tree = ET.parse(xmlfile)
		ET.dump(tree)
		ET.register_namespace('urn:jboss:domain:1.4', 'xmlns')
		self._root = tree.getroot()
	@property
	def root(self):
		return self._root

	@staticmethod
	def nstag(element):
		ns, tag = element.split('}')
		return ns[1:], tag

	def sector(self, pattern):
		for elem in self._root:
			if pattern in elem.tag:
				return [elem for elem in elem.findall('.//')]






if __name__ == '__main__':
	# module debugging area
	print('\n'.join(m for m in dir()))
	xmlfile = '%s/.cliboss/sppxml/accspptest01_s0.xml'%(os.path.expanduser('~'))
	xml = JBossXML(xmlfile)
	for sector in xml.sector('management'):
		print(sector)
	#	print(elem.tag, elem.attrib, elem.text)
