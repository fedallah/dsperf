#!/usr/bin/env python3

import csv
import sqlite3

# requires python3
# requires sqlite3
#

sqldb = sqlite3.connect(':memory:')

def main:
	while True:
		input_location = input("Please provide the pathname of the file you wish to extract data from.  Enter a blank line when you are done.")
		if input_location = False:
			break
		else:
			mi = inputfile(input_locaton)
			allinputs.append(mi)
			mi = False
	for ifile in allinputs:
		

class inputfile:
	def __init__(self, location):
		self.location = location
		if not os.path.isfile(self.location):
			print "file not found"
		open( self.location, newline='' ) as csvfile
		csvread = csv.rader( csvfile, delimiter=',' quotechar='' )
		
class perfitem_group(inputfile):
	def __init__(self)
	def 

class perfitem(perfitem_group):
	def __init__(self)
	def mkdict
		
		
		
		
class row(inputfile):
	def init(self):
		self = 
		
		with open( inputfile.self.location, newline='' ) as csvfile:
		csvread = csv.reader( csvfile, delimiter=',', quotechar='' )
	def get:
		return row



allfiles = False

while True:
	

# while allfiles <> "":