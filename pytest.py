#!/usr/bin/env python3

import sqlite3
from datetime import datetime

class InputFile:
	def __init__(self, path):
		self.path = path
		thisfile = open(self.path)
	def GetRawData():
		c = 0
		for row in thisfile:
			c += 1
			row = row.rstrip('\r\n')
			row = row.split(',', 11)
			# input conversion and validation
			if len(row) == 12:
				ic = 0
				while ic < 13:
					if ( ic == 0 ) or ( ic > 1 and ic < 5 ):
						# no error is required here; this is pretty hard to screw up
						valrow[ic] = str(row[ic])
					elif ic == 1:
						try:
							valrow[1] = datetime.strptime(row[1], '%x, %X')
						except:
							errstr = "(Invalid entry of date/time stamp at row ${:d} with path ${:s})".format(c, self.path)
							raise InputErr(errstr)
					elif ( ic == 5 ):
						try:
							valrow[ic] = int(row[ic])
						except:
							errstr = "(Invalid entry of something that isn't an integer where integer expected at row ${:d} with path ${:s})".format(c, self.path)
							raise InputErr(errstr)
					elif ( ic > 5 ):
						try:
							valrow[ic] = float(row[ic])
						except:
							errstr = "(Invalid entry of something that isn't a float where float expected at row ${:d} with path ${:s})".format
							raise InputErr(errstr)
					ic += 1
				rawdata.append(valrow)
			else:
				errstr = "(Invalid input at row ${:d} with path ${:s})".format(c, self.path)
				raise InputErr(errstr)
		if ( len(valrow) > 0 ) and ( c > 0 ):
			return rawdata
		else:
			return "ERROR - please check input!\n"
		
class StorageSystem:
	def __init__(self, name, db_h):
		self.name = name
		self.db_h = db_h
	def ImportData():
		impstr = "CREATE TABLE %s (system_name text, datewritten timestamp, controllerA text, controllerB text, logical_drive text, total_iops int, read_pct float, cache_hit_pct float, curent_kbs float, max_kbs float, current_iops float, maximum_iops float)" % ("")
		self.db_h.executemany( '' )
		self.db_h.commit()
	def FetchData():
		self.db_h.execute
		
	
def main():
	try:
		sqldb = sqlite3.connect(':memory:')
	except:
		raise dberr("SQLite database could not be created in memory, or you lack sufficient permissions, etc.")

	sqldb.execute ( 'create table storage_data ( system_name text, datewritten timestamp, controllerA text, controllerB text, logical_drive text, total_iops int, read_pct float, cache_hit_pct float, curent_kbs float, max_kbs float, current_iops float, maximum_iops float )' )

	allperfdata = []
	while True:
		floc = input("Enter pathname: ")
		if floc == "":
			break
		else:
			thisfile = open(floc)
			for row in thisfile:
				row = row.rstrip('\r\n')
				perfobj = row.split(',', 11)
				allperfdata.append(perfobj)

	sqldb.executemany( 'INSERT INTO storage_data VALUES( ?,?,?,?,?,?,?,?,?,?,?,? )', allperfdata )
	sqldb.commit()

	all_ssdb = sqldb.execute( 'SELECT DISTINCT system_name FROM storage_data' )
	all_storagesystems = all_ssdb.fetchall()



sqldb.close()

# all_storagesystems = sqldb.execute( 'SELECT DISTINCT system_name FROM storage_data' )
# all_timestamps = sqldb.execute( 'SELECT DISTINCT datewritten FROM storage_data' )

# all_storagedata = sqldb.execute( 'SELECT DISTINCT ON (system_name, datewritten) * FROM storage_data GROUP BY system_name ORDER BY system_name, datewritten desc' )

# testout = all_storagedata.fetchall()

# print(testout)
