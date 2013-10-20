#!/usr/bin/env python3

import sqlite3
import json
from datetime import datetime

class InputFile:
	def __init__(self, path):
		self.path = path
		with open(self.path) as fm:
			valrow = fm.readline()
			
			
	def Dump():
		fh = open(self.path)
		for row in fh:
			return row
		close fh

class PerfObj(InputFile):
	def __init__(self, csv_input):
		self.ilist = row.split(',', 11)
		