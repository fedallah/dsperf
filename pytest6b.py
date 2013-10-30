#!/usr/bin/env python3

import sqlite3
from hashlib import sha256
from random import getrandbits
from numpy import std
from numpy import median

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

class Analyze:
	'''
	A toolbox that provides some useful analytics (e.g. standard deviation).
	'''
	SDevCalc = std	# initialize for standard deviation
	MedCalc = median	# initialize for median.
	def __init__(self):
		'''
		Nothing is really going on here.
		'''
		return None
	def CalcStd(inlist):
		'''
		Accepts a list of tuples with keys (probably dates/times) and values.
		Returns this same list of tuples with two values appended: the input value's
		relative deviation from the median in terms of (positive or negative)
		deviations from sigma, and an integer result of this same number.
		'''
		input_arr = []
		for i in inlist:
			if isinstance(i, tuple):
				input_arr.append(i[1])
			else:
				raise ValueError(' : no tuple found where tuple expected.')
				return False
		# calculate standard deviation and median
		med = MedCalc(input_arr)
		sd = SDevCalc(input_arr)
		# bound for sigma max and min
		# sigma min:
		sigmaMin = med
		sigma = 0
		sMap = {}
		while sigmaMin > min(input_arr):
			uBsigmaMin = sigmaMin
			sigma += 1
			sigmaMin = med - ( sd * sigma )
			sMap[(sigma * -1)] = ( sigmaMin, uBsigmaMin )
		# sigma max (similar, but non negative)
		sigmaMax = med
		sigma = 0
		while sigmaMax < max(input_arr):
			lBsigmaMax = sigmaMax
			sigma += 1
			sigmaMax = med + ( sd * sigma )
			sMap[sigma] = ( lBsigmaMax, sigmaMax )
		# calculate deviance (in terms of multiples of sigma) for each value in inlist
		# we'll be tupling this up with the input and pushing it to an output list.
		outList = []
		while len(inlist) > 0:
			worker = inlist.pop()
			if ( worker[1] == med ):
				varSig = 0
				sigmaO = 0
			else:
				for sigmaInt in sMap.keys():
					range = sMap[sigmaInt]
					# is it in range?
					if ( worker[1] >= range[0] ) and ( worker[1] < range[1] ):
						if ( sigmaInt < 0 ):
							varSig = ( ( range[1] - worker[1] ) / sd ) + sigmaInt
							sigmaO = sigmaInt
						elif ( sigmaInt > 0 ):
							varSig = ( ( worker[1] - range[1] ) / sd ) + sigmaInt
							sigmaO = sigmaInt
						break
					else:
						continue
			outList.append( (worker[0], worker[1], varSig, sigmaO) )
		return outList
	def StdOnly(inlist):
		'''
		Returns only the standard deviation as a float - no list, nothing - just the measure
		of variance.  Accepts a standard list (no nesting).
		'''
		return SDevCalc(inlist)

'''
The following is specific for the Exchange arrays ( e.g. file schemas
used will differ).
'''

schemMap = {}
schemMap[1] = ( 'SYSTEM_NAME', 'TEXT' )
schemMap[2] = ( 'DATE', 'DATE' )
schemMap[3] = ( 'TIME', 'TIME' )
schemMap[4] = ( 'DAY_OF_WEEK', 'TEXT' )
schemMap[5] = ( 'CONT-SYS-LD_NAME', 'TEXT' )
schemMap[6] = ( 'TOTAL_IOPS', 'FLOAT' )
schemMap[7] = ( 'READ_PCT', 'FLOAT' )
schemMap[8] = ( 'CACHE_HIT_PCT', 'FLOAT' )
schemMap[9] = ( 'CURRENT_KBPS', 'FLOAT' )
schemMap[10] = ( 'MAX_KBPS', 'FLOAT' )
schemMap[11] = ( 'CURRENT_IOPS', 'FLOAT' )
schemMap[12] = ( 'MAXIMUM_IOPS', 'FLOAT' )

ds47xSchem = Schema(schemMap)

aDBcon = sqlite3.connect(':memory:')
aDBcur = aDBcon.cursor()

ifile = None
while ifile != 99:		
	ifile = input('Please enter the fully qualified path to an input file from IBM DS4700 arrays USUS1SAN1010 or USUS1SAN1020 :')