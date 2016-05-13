#!/usr/bin/env python2

# stdlib import
import yaml, json

# local relative import
from modules import jboss7, jboss7_cli


def main():
	trgcfg = 'target.json'
	def _json2jbcfg(jboss_config):
		with open(jboss_config, 'r') as jsn:
			return json.load(jsn)
	jbcfg = _json2jbcfg(trgcfg)

	#print(jbcfg)
	print(jboss7.status(jbcfg))
	print(jboss7.list_deployments(jbcfg))
	print(jboss7.read_datasource(jbcfg, 'HasHistoryServiceDS'))

main()
