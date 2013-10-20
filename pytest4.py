#!/usr/bin/env python3

import sqlite3
from datetime import datetime

class InputFile:
	def __init__(self, path)
		self.path = path
		try:
			self.ifile = open(self.path)
		except IOError:
			print "File does not exist or cannot be opened."
		first_val = self.ifile.readline()
		isval = first_val.split(',', 11)
		if ( len(mo) != 12 ):
			raise InvalidInFile