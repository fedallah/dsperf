#!/usr/bin/env python3

import sqlite3
from datetime import datetime

class InputFile:
	def __init__(self, path)
		self.path = path
		try:
			with open(self.path) as ifile:
				first_val = ifile.readline()
				isval = first_val.split(',', 11)
				if ( len(isval) != 12 ):
					raise AttributeError(' : Found ' + str(len(isval)) + ' fields in first line of input file at ' + self.path + ' where 12 expected.  This does not look like a valid file.')
		except IOError:
			print('Could not open a file at this location.  Are you sure it exists?')
	def dump(self):
		with open(self.path) as ifile:
			for line in ifile:
				return line			

class PerfObj(InputFile):
	def __init__(self, raw_in)
