#!/usr/bin/env python3

import sqlite3
import re

# requires python3
# requires sqlite3

sqldb = sqlite3.connect(':memory:')

class FileGroup:
	def __init__(self, comment=False):
		self.comment = comment
	
class InputFile(FileGroup):
	def __init__(self, location):
		self.location = location
		try:
			fm = open(self.location, newline='')
		except:
			raise fileprob("The file could not be opened or found.")
	def printall():
		for row in fm:
			return row
		
class PerfItem(InputFile):
	def __init__(self, mo):
		item = mo.split(',', -1)
	def dbsend():
		sqldb.execute( 'INSERT INTO storage_data VALUES( ?,?,?,?,?,?,?,?,?,? )', item )



def main():
	sqldb.execute('CREATE TABLE storage_data ( sys_name text, datewritten timestamp, ip_cA text, ip_cB text, subsys_name text, total_iops int, read_pct float, cache_hit_pct float, current_kbs float, max_kbs float, current_iops float, max_iops float )')
	fg0 = FileGroup()
	print fg0
	while True:
		file_loc = input("Please enter the location of the file you wish to analyze (or an empty line to quit: ")
		if file_loc == "":
			break
		else:
			inf = fg0.InputFile( file_loc )
	for f in fg0:
		for i in f:
			pi = i.printall
			pi.dbsend

	
	sqldb.execute('SELECT DISTINCT ON (sys_name) sys_name FROM storage_data')
	
main()