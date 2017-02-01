#!/usr/bin/env /usr/bin/python3
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
"""module disclaimer"""

# global & stdlib imports
import re
import os
import sys
from socket import getfqdn as fqdn

from colortext import blu, yel, error
from net import askdns, netcat as nc, SecureSHell as SSH
ssh = SSH()

def listhosts(stageha):
	servers = []
	for i in range(1, 20):
		if askdns(stageha+str(0)+str(i)):
			servers.append(fqdn(stageha+str(0)+str(i)))
		elif askdns(stageha+str(i)):
			servers.append(fqdn(stageha+str(i)))
		elif askdns(stageha):
			if not servers:
				servers.append(fqdn(stageha))
		else:
			break
	return servers if servers else [stageha]

def listclusters(name):
	stages = ('dev', 'test', 'cert', 'ac1', 'prod', 'build')
	stageha = re.sub('\d{1,2}$', '', name)
	name = re.sub('^(ac1)|(dev|test|cert|build)?$', '', stageha)
	cluster = {}
	for stage in stages:
		stageha = name
		if stage == 'ac1':
			stageha = stage+name
		elif stage == 'prod':
			stageha = name
		else:
			stageha = name+stage
		hosts = listhosts(stageha)
		if hosts:
			cluster[stage] = hosts
	return cluster

def slotdir(fqdn, slotno):
	slotdir = ssh.stdx(
	    'ls /home/jboss/ |egrep -i "^slot\-?%s$"'%(slotno),
	    host=fqdn, user='root')
	if slotdir:
		return slotdir.strip()

def jolofix(fqdn, slotno):
	sltdir = slotdir(fqdn, slotno)
	print(
	    blu('searching on'), yel(fqdn),
	     blu('for appropriate jolokia war file to slot'), yel(sltdir))
	out = ssh.stdo(
	    'find /home/jboss -type f -name "jolokia*.war"',
	     host=fqdn, user='root')
	if out:
		jololns = out.split('\n')
		slotln = [l for l in jololns if sltdir in l]
		if slotln:
			jololn = slotln[0]
		elif jololns:
			jololn = jololns[0]
		if jololn:
			print(blu('touching'), yel(jololn))
			ssh.call('touch %s' %(jololn), host=fqdn, user='root')









if __name__ == '__main__':
	# module debugging area
	print('\n'.join(d for d in dir()))
	#print(listclusters('accfufiboss'))
	#print(listclusters('accjenkins'))
