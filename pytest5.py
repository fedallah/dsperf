#!/usr/bin/env python3

import sqlite3
import re
from datetime import datetime
from hashlib import sha256

def globalVerbose(isOn, v_input):
	"""
	Provide an easy interface to print method input on demand
	"""
	if v_input is True:
		print('VERBOSE: input is as follows: --- \n\t' + str(v_input) + '\n --- END VERBOSE')
		return True
	else:
		return False

def mkCSV(origIter):
	"""
	Create CSV output from an iterable object.  This function is ripe for reuse elsewhere.
	"""
	elems = None
	allElems = None
	for elem in origIter:
		if not allElems:
			allElems = ('\"' + str(elem) + '\"')
		else:
			allElems = (allElems + ',' + '\"' + str(elem) + '\"')
	return allElems	

class Schema:
	"""
	Provides an interface to define, export, and verify the correct schema for our input program-wide.  Dictionary keys are
	both key names for class PerfObj and column names for a relational database.  Values are SQL-compatible data types (e.g.
	"TEXT", "CHAR(64)", "FLOAT", "INT", et al.
	"""
	def __init__(self, schemaMapIn):
		# Construct; accept a dictionary object.
		if isinstance(schemaMapIn, dict):
			self.schemaMap = schemaMapIn
			return None
		else:
			raise ValueError(' : tried to pass something other than a dictionary object where a dictionary is expected.')
			return False
	def DictInputChk(self, dictInput):
		# Validate that input is a dictionary and that keys match with self, return bool accordingly
		if (isInstance(dictInput), dict) and (dictInput.keys() == self.schemaMap.keys()):
			return True
		else:
			return False
	def DictOut(self):
		# return input dictionary
		return self.schemaMap
	def Titles(self):
		# return a tuple of input keys
		return tuple(self.schemaMap.keys())
	def Types(self):
		# return a tuple of output SQL-compatible types
		return tuple(self.schemaMap.values())
	
class InputFile:
	"""
	InputFile ingests a standard comma-delimited file produced by smcli.  It helps to sanitize and verify the file, and 
	output its data for other classes in a compatible and performant way.
	"""
	rm_trailcomma = re.compile(',{1}$|,{1}\n')
	def __init__(self, path):
		"""
		Instantiate, open the input file, and validate the first line of input.
		"""
		self.path = path
		try:
			first_val = (open(self.path), 'Ur').readline()
			if first_val.count(',') != 12:
				raise AttributeError(' : Found ' + str(len(isval)) + ' fields in first line of input file at \"' + str(self.path) + '\" where 12 expected.  This does not look like a valid file.')
				return False
			else:
				continue
			return None
		except:
			raise IOError(' : could not open file on class InputFile for constructor method at location \"' + str(self.path) + '\".  Aborting.')
			return False
	def Dump(self):
		"""
		Validate each line of input and remove a trailing comma.  Make a SHA256 hash of the plaintext string.
		Split the string into a list, append the aforementioned SHA256 hash, then convert the list into a tuple.
		"""
		try:
			with open(self.path, 'Ur', encoding='utf-8') as inputfile:
				for line in inputfile:
					if ( len(line) > 0 ) and ( line.count(',') == 12 ):
						hashme = sha256()	# init sha256sum method from hashlib
						line = re.sub(rm_trailcomma,'',line)
						hashme.update(line.encode(inputfile.encoding))
						line = line.split(',', 11)
						line.append(str(hashme.hexdigest()))
						yield tuple(line) # return a generator object!
					else:
						continue
		except:
			raise IOError(' : could not open file on class InputFile for method \'Dump\' at location \"' + str(self.path) + '\".  Aborting.')
			return False

class PerfObj:
	"""
	PerfObj accepts a single, static tuple as input on its constructor method.  It uses this the position
	of each value in this tuple to construct and validate a dictionary, parsing date and time and casting
	types where necessary.  It then provides a variety of useful output methods - CSV, tuple, dictionary, etc.
	"""
	# get_controller and get_LD: regex 'class variables' instatiated for the use of every object; they are used by constructor
	get_controller = re.compile(',CONTROLLER IN SLOT (\w{1}),')
	get_LD = re.compile(',Logical Drive (.*?),')
	def __init__(self, u_input, validSchema, verbose = False, verbose_func = globalVerbose):
		"""
		Validate and construct.
		"""
		verbose_func(verbose, u_input)
		if isinstance(u_input, tuple):
			if len(u_input) == 12:
				self.dictout = {}
				# map input to dictionary.
				self.dictout[validSchema[0]] = str(u_input[0])
				self.dictout[validSchema[1]] = datetime.strptime(u_input[1])
				self.dictout[validSchema[2]] = str(u_input[2])
				self.dictout[validSchema[3]] = str(u_input[3])		
				if ( get_controller.search(u_input[4]) ) and ( get_LD.search(u_input[4]) ):		# is this input for a controller or a logical drive?  It cannot be for both.
					raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\' - both controller and logical drive found where only one expected')
					return False
				elif get_controller.search(u_input[4]):
					self.dictout[validSchema[4]] = str(get_controller.search(u_input).group(1))
					self.dictout[validSchema[5]] = None
				elif get_LD.search(u_input[4]):
					self.dictout[validSchema[4]] = None
					self.dictout[validSchema[5]] = str(get_LD.search(u_input).group(1))
				else:
					raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\'')
					return False
				self.dictout[validSchema[6]] = int(u_input[6])
				self.dictout[validSchema[7]] = float(u_input[7])
				self.dictout[validSchema[8]] = float(u_input[8])
				self.dictout[validSchema[9]] = float(u_input[9])
				self.dictout[validSchema[10]] = float(u_input[10])
				self.dictout[validSchema[11]] = float(u_input[11])
				self.dictout[validSchema[12]] = float(u_input[12])
				self.dictout[validSchema[13]] = str(u_input[13])
				return None	# on successful construction
			else:
				raise AttributeError(' : Found ' + str(len(u_input)) + ' fields in input string:\n' + u_input + '\n... where 12 expected on class \'PerfObj\', constructor method.  Invalid input.')
				return False
		else:
			raise ValueError(' : class PerfObj received non-tuple input on constructor where tuple expected; cannot continue.')
			return False
	def CSVOut(self, genCSVfunc = mkCSV, dictInput = self.dictout, validSchema, inputChk = globalDictInputChk, printSchema = False, verbose_func = globalVerbose, verbose = False):
		"""
		Return CSV output of self.dictout (default) or a similar dictionary object.
		Print this object's schema if asked to do so (default to no).
		"""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, validSchema):
			allVals = None
			for key in validSchema:
				allVals.append(dictInput[key])
			if len(allVals) == 13:
				if printSchema:
					return(genCSVfunc(validSchema) + '\n' + genCSVfunc(allVals))
				else:
					return(genCSVfunc(allVals))
			else:
				# fail and return none if fewer than 13 output values found, as this is indicative of invalid input.
				raise ValueError(' : fewer than required number of output values found with standard global validSchema on method CSVOut.  You are likely passing a miskeyed dictionary.')				
				return False
		else:
			return False
	def DictOut(self, dictInput = self.dictout, validSchema, inputChk = globalDictInputChk, verbose_func = globalVerbose, verbose = False):
		"""
		Return a dictionary after validation.
		"""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, validSchema):
			return dictInput
		else:
			return False
	def TupleOut(self, validSchema, dictInput = self.dictout, inputChk = globalDictInputChk, verbose_func = globalVerbose, verbose = False)
		"""
		Return a tuple based on a dictionary after validation, using provided validSchema.
		"""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, validSchema):
			prelist = []
			for elem in validSchema:
				prelist.append(dictInput[elem])
			return tuple(prelist)
		else:
			return False

class DSPerfDB_SQLite3:
	"""
	Initializes an SQLite3 database.  Provides a standard interface for table creation and data extraction
	without needing to manually write SQL (although that is an option).
	"""
	def __init__(self, location = ':memory:', tableName = )
		"""
		Construct, connect, provide a cursor object.  Default database location is in memory, although this really
		is arbitrary.
		"""
		self.con = sqlite3.connect(location)
		self.cur = self.con.cursor()
		return None
	def CreateTable(self, tableName, tableSchemaDict, verbose = False)
		"""
		Create a table using provided schema.  Using the schema class provided up above is really a smart idea here,
		although it is hardly a requirement.
		"""
		if isinstance(tableSchemaDict, dict):
			ColCt = 0
			ColTot = len(tableSchemaDict)
			iString = None
			for i in tableSchemaDict:
				ColCt += 1
				if ColCt == 1:
					iString = 'CREATE TABLE ' + str(tableName) + ' (' + str(i) + ' ' + str(tableSchemaDict[i])
				elif ColCt > 1:
					iString = iString + ', ' + str(i) + ' ' + str(tableSchemaDict[i])
			iString = iString + ')'
			if verbose:
				print(str(iString))
			self.cur.execute(iString)
			self.con.commit()
			return True
		else:
			raise ValueError(' : invalid input for schema - requires type dict')
			return False
	def ListTables(self):
		return self.cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
	def ListDateRange(self, table, datecol):
	def SelectFromTable(self, table, datemin, datemax
	def Close(self):
		self.con.close()