#!/usr/bin/env python3
# global imports
import os
import sys
from xml.etree import ElementTree as ET
# local relative imports
# default vars
__me__ = os.path.basename(__file__)
__at__ = os.path.dirname(
    os.path.abspath(__file__)
    ) if not os.path.islink(
        os.path.dirname(os.path.abspath(__file__))
    ) else os.readlink(os.path.dirname(os.path.abspath(__file__)))
__version__ = '0.0'


class XmlListConfig(list):
	def __init__(self, aList):
		for element in aList:
			if element:
				if len(element) == 1 or element[0].tag != element[1].tag:
					self.append(XmlDictConfig(element))
				elif element[0].tag == element[1].tag:
					self.append(XmlListConfig(element))
			elif element.text:
				text = element.text.strip()
				if text:
					self.append(text)

class XmlDictConfig(dict):
	def __init__(self, parent_element):
		if parent_element.items():
			self.updateShim(dict(parent_element.items()))
		for element in parent_element:
			if len(element):
				aDict = XmlDictConfig(element)
				if element.items():
					aDict.updateShim(dict(element.items()))
				self.updateShim({element.tag: aDict})
			elif element.items():
				self.updateShim({element.tag: dict(element.items())})
			else:
				self.updateShim({element.tag: element.text})

	def updateShim(self, aDict):
		for key in aDict.keys():
			if key in self:
				value = self.pop(key)
				if type(value) is not list:
					listOfDicts = []
					listOfDicts.append(value)
					listOfDicts.append(aDict[key])
					self.update({key: listOfDicts})
				else:
					value.append(aDict[key])
					self.update({key: value})
			else:
				self.update(aDict)


def dicprint(xdict, delim=0):
	def _lisprint(xlist, delim):
		for lis in xlist:
			if isinstance(lis, dict):
				dicprint(lis, delim)
			print(c for c in lis)
	for (sector, configs) in sorted(xdict.items()):
		print('%s%s = %s'%(delim*'\t', sector, configs))
		delim+=1
		if isinstance(configs, dict):
			dicprint(configs, delim)
		elif isinstance(configs, list):
			for cfg in configs:
				if isinstance(cfg, dict):
					dicprint(cfg, delim)
				elif isinstance(cfg, list):
					_lisprint(cfg, delim)
		delim-=1



if __name__ == '__main__':
	# module debugging area
	print('\n'.join(m for m in dir()))
	xml = '%s/.cliboss/sppxml/accspptest01_s0.xml' %(os.path.expanduser('~'))
	tree = ET.parse(xml)
	root = tree.getroot()
	xmldict = XmlDictConfig(root)
	print(root.tag)
	dicprint(xmldict)

#			elif confs and type(confs) is list:
#				print('\n\t\t '.join(conf for conf in confs))
#			elif confs:
#				print('\t\t', confs)
