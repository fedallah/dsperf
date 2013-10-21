#!/usr/bin/env python3
import csv
import sqlite3
import re
import sys

dsfile = input("Please provide the pathname of the file you wish to extract data from: ")

try:
	dbloc_d = './dsperfdb.sqlite3'
	dbcon = sqlite3.connect(dbloc_d)
except IOError:
	print "Could not locate SQLite DB at default location " + dbloc_d + "." 
	dbloc = input("Please provide the fully qualified path of the database file: ")
	dbcon = sqlite3.connect(dbloc)
except IOError:
	open(dbloc_d)
	close(dbloc_d)
	print "Could not open " + dbloc + " - defaulting to default " + dbloc_d
	dbcon = sqlite3.connect(dbloc_d)
except:
	raise sql_noconn('Unexpected error opening sqlite database for performance analysis.  Could not open user-defined or default locations.')
	sys.exit(15)

with open('', newline='') as csvfile:
	dsreader = csv.reader(csvfile, delimiter=',', quotechar='')
	for row in dsreader:
		