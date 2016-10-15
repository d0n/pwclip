#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt

from system.random import biggerrand, lowerrand

def maxprime(stop, start=3):
    start = start if start%2 != 0 else start+1
    for i in reversed(range(start, stop, 2)):
        if all(int(i%j) for j in range(3, int(sqrt(i))+1, 2) if j):
            return i

def dhnums(sec):
	while True:
		rnd = biggerrand(sec)
		pri = maxprime(rnd**2)
		if pri > rnd:
			break
	return rnd, pri

def dhsecs():
	return lowerrand(99999), lowerrand(99999)

def dhcompile(sec, rnd, pri):
	return int(int(rnd**sec)%pri)

def dhprep(sec):
	while True:
		rnd, pri = dhnums(sec)
		gen = dhcompile(sec, rnd, pri)
		if gen > 1:
			break
	return rnd, pri, gen

def dhsend():
	sec = lowerrand(99999)
	rnd, pri, gen = dhprep(sec)
	print(sec)
	print(rnd, pri, gen)
	res = int(input())
	return dhcompile(sec, res, pri)

def dhrecv(rnd, pri, gen):
	sec = lowerrand(99999)
	print(sec)
	print(dhcompile(sec, rnd, pri))
	return dhcompile(sec, gen, pri)

