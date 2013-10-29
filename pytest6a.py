#!/usr/bin/env python3

import sqlite3
from hashlib import sha256
from random import getrandbits

def mkSHA256(input):
	shaObj = sha256
	return shaObj((str(input).encode('utf-8'))).hexdigest()

class Schema:
	'''
	Provides an interface to define, export, and verify the correct
	schema for our input to the database (and beyond!)  Keys are a
	nonzero integer.  This integer should correspond with a left-to-right column location
	(with the leftmost being zero, and so on).
	Values are a tuple: the first field is a 
	column name; the second is its data type (compatible with
	whatever RMDBS you are using.  For example:
	schemaMapIn[0] = ( 'IOWaitTime', 'INT' )
	We'll be using this to validate and cast input, as well as to 
	construct our database tables.
	'''
	def __init__(self, schemaMapIn):
		'''
		Construct, validating input.  Return False if input is invalid.
		'''
		if isinstance(schemaMapIn, dict):
			valIn = len(schemaMapIn)
			valC = 0
			for moVal in schemaMapIn.values():
				if not isinstance(moVal, tuple):
					raise ValueError(' : tuple not found where tuple expected')			
					return False
			self.schemaMap = schemaMapIn
			return None
		else:
			raise ValueError(' : dict not found where dict expected')
			return False
	def DictInputChk(self, dictInput):
		'''
		Validate that input is a dictionary and that its keys are equivalent
		to schema provided.
		'''
		if (isinstance(dictInput, dict) and (dictInput.keys() == self.schemaMap.keys()):
			return True
		else:
			return False
	def AutoCast(self, TupleIn):
		'''
		Attempt to autocast an input tuple based on self.schemaMap and some sensible guesses.
		The tuple should be arranged as ('column name', 'value').  Return the cast value.
		If you can't figure out what it is, don't change it at all - return it as it was.
		This is intentionally quite conservative.
		'''
		if ( TupleIn[0] in self.schemaMap ):
			if ( TupleIn[0] == 'TEXT' or 'VARCHAR' or 'CHAR' ):
				return str(TupleIn[1])
			elif ( TupleIn[0] == 'INT' ):
				return str(TupleIn[1])
			elif ( TupleIn[0] == 'FLOAT' ):
				return float(TupleIn[1])
			else:
				return TupleIn[1]
	def DictOut(self):
		'''
		Return input dictionary, nothing more.
		'''
		return self.SchemaMap
	def SQLDict(self):
		'''
		Return a dictionary appropriate for use in the 'CreateTable' method
		of 'DSPerfDB_SQLite3' and friends.
		'''
		SQL_out = {}
		for moi in self.SchemaMap.Values():
			SQL_out[moi[0]] = moi[1]
		return SQL_out
	def Titles(self)
		'''
		Return a tuple of input keys - i.e. the titles of all columns
		'''
		return tuple(self.SchemaMap.keys())

class PerfDB_SQLite3:
	'''
	Initializes a SQLite3 database.  Provides a standard interface for table creation
	and data extraction without having to manually write SQL.  You don't need
	to use this class if you don't need or want to, but it does provide some useful
	functions out-of-the-box.
	'''
	def __init__(self, dbLoc = ':memory:'):
		'''
		Construct with the database location (defaults to in-memory).
		'''
		self.con = sqlite3.connect(dbLoc)
		self.cur = self.con.cursor()
	def CreateTable(self, tableName, schemaInDict)
		'''
		Creates a table in our SQLite database using tableName (self-explanatory)
		and schemaInDict - a dictionary consisting of key-value pairs of column
		names and SQL types.  See method 'SQLDict' on class 'Schema' if you need
		help figuring this out.
		'''
		if isinstance(schemaInDict, dict):
			ColCt = 0
			ColTot = len(schemaInDict)
			iString = None
			for i in schemaInDict:
				iString = '
		else:
			raise ValueError(' : invalid input - dict not found where dict expected')
			return False