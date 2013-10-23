#!/usr/bin/env python3

import sqlite3
from datetime import datetime
import re

# global schema to be used across all classes.  This is immutable and should only ever be stored here in this tuple!
globalSchema = 'system_name', 'timestamp', 'IPaddr_controllerA' 'IPaddr_controllerB', 'controllerTotal', 'LogicalDriveName', 'total_IOPS', 'read_percent', 'cache-hit_percent', 'current_KBsec', 'max_KBsec', 'current_IOPS', 'max_IOPS'

def globalSchemaInit(name = False, type = False):
	schemaMap = {}
	schemaMap['system_name'] = 'TEXT'
	schemaMap['timestamp'] 	= 'DATETIME'
	schemaMap['IPaddr_controllerA'] = 'TEXT'
	schemaMap['IPaddr_controllerB'] = 'TEXT'
	schemaMap['controllerTotal'] = 'TEXT'
	schemaMap['LogicalDriveName'] = 'TEXT'
	schemaMap['total_IOPS'] = 'INT'
	schemaMap['read_percent'] = 'FLOAT'
	schemaMap['cache-hit_percent'] = 'FLOAT'
	schemaMap['current_KBsec'] = 'FLOAT'
	schemaMap['max_KBsec'] = 'FLOAT'
	schemaMap['current_IOPS'] = 'FLOAT'
	schemaMap['max_IOPS'] = 'FLOAT'
	if schemaMap:
		if name and type:
			return tuple(schemaMap.values()), tuple(schemaMap.keys())
		elif name:
			return tuple(schemaMap.keys())
		elif type:
			return tuple(schemaMap.values())
		else:
			return tuple(schemaMap.keys())	# default - return keys only if caller does not specify
	else:
		raise ValueError(' : no schema defined, nothing to output.')
		return None

def globalDictInputChk(dictInput, tableSchema = globalSchema):
	"""
	Check for valid or invalid input: is our input a dictionary?  Is it congruent with provided tableSchema (default globalSchema)?
	This function should be valid for use in class PerfObj and elsewhere.
	"""
	if ( isinstance(dictInput, dict) and ( list(dictInput.keys()).sort() == list(tableSchema).sort() ) ):
		return True
	else:
		raise ValueError(' : input ' + str(dictInput) + ' is either not a dictionary or has keys that do not comply with the enforced schema.')
		return False

def globalVerbose(isOn, v_input):
	"""Provide an easy interface to print method input on demand"""
	if v_input is True:
		print('VERBOSE: input is as follows: --- \n\t' + str(v_input) + '\n --- END VERBOSE')
		return True
	else:
		return None

def mkCSV(origIter):
	"""Create CSV output from an iterable object.  This function is ripe for reuse elsewhere."""
	elems = None
	allElems = None
	for elem in origIter:
		if not allElems:
			allElems = ('\"' + str(elem) + '\"')
		else:
			allElems = (allElems + ',' + '\"' + str(elem) + '\"')
	return allElems	

class InputFile:
	"""
	InputFile ingests a standard comma-delimited file produced by smcli.  It helps to sanitize and verify the file, and 
	output its data for other classes in a compatible and performant way.
	"""
	rm_trailcomma = re.compile(',{1}$|,{1}\n')
	def __init__(self, path):
		"""Instantiate, open the input file, and validate the first line of input."""
		self.path = path
		try:
			first_val = (open(self.path)).readline()
			if first_val.count(',') != 12:
				raise AttributeError(' : Found ' + str(len(isval)) + ' fields in first line of input file at \"' + str(self.path) + '\" where 12 expected.  This does not look like a valid file.')
				return None
			else:
				continue
		except:
			raise IOError(' : could not open file on class InputFile for constructor method at location \"' + str(self.path) + '\".  Aborting.')
			return None
	def Dump(self):
		"""Validate each line of input and remove a trailing comma.  Return a generator object."""
		try:
			for line in open(self.path):
				if ( len(line) > 0 ) and ( line.count(',') == 12 ):
					line = re.sub(rm_trailcomma,'',line)
					line = line.split(',', 11)
					yield line	# return a generator object!
				else:
					continue
		except:
			raise IOError(' : could not open file on class InputFile for method \'Dump\' at location \"' + str(self.path) + '\".  Aborting.')
			return None

class PerfObj:
	"""
	PerfObj accepts a single, static tuple as input on its constructor method.  It uses this the position
	of each value in this tuple to construct and validate a dictionary, parsing date and time and casting
	types where necessary.  It then provides a variety of useful output methods - CSV, tuple, dictionary, etc.
	"""
	# get_controller and get_LD: regex 'class variables' instatiated for the use of every object; they are used by constructor
	get_controller = re.compile(',CONTROLLER IN SLOT (\w{1}),')
	get_LD = re.compile(',Logical Drive (.*?),')
	def __init__(self, u_input, tableSchema = globalSchema, verbose = False, verbose_func = globalVerbose ):
		self.dictout = {}
		verbose_func(verbose, u_input)
		if isinstance(u_input, tuple):
			if len(u_input) == 12:
				# map input to dictionary.
				self.dictout[tableSchema[0]] = str(u_input[0])
				self.dictout[tableSchema[1]] = datetime.strptime(u_input[1])
				self.dictout[tableSchema[2]] = str(u_input[2])
				self.dictout[tableSchema[3]] = str(u_input[3])		
				if ( get_controller.search(u_input[4]) ) and ( get_LD.search(u_input[4]) ):		# is this input for a controller or a logical drive?
					raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\' - both controller and logical drive found where only one expected')
				elif get_controller.search(u_input[4]):
					self.dictout[tableSchema[4]] = str(get_controller.search(inp).group(1))
					self.dictout[tableSchema[5]] = None
				elif get_LD.search(u_input[4]):
					self.dictout[tableSchema[4]] = None
					self.dictout[tableSchema[5]] = str(get_LD.search(inp).group(1))
				else:
					raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\'')
					return None
				self.dictout[tableSchema[6]] = int(u_input[6])
				self.dictout[tableSchema[7]] = float(u_input[7])
				self.dictout[tableSchema[8]] = float(u_input[8])
				self.dictout[tableSchema[9]] = float(u_input[9])
				self.dictout[tableSchema[10]] = float(u_input[10])
				self.dictout[tableSchema[11]] = float(u_input[11])
				self.dictout[tableSchema[12]] = float(u_input[12])
				return True
			else:
				raise AttributeError(' : Found ' + str(len(u_input)) + ' fields in input string:\n' + u_input + '\n... where 12 expected on class \'PerfObj\', constructor method.  Invalid input.')
				return None
		else:
			raise ValueError(' : class PerfObj received non-tuple input on constructor where tuple expected; cannot continue.')
			return None
	def CSVOut(self, genCSVfunc = mkCSV, dictInput = self.dictout, tableSchema = globalSchema, inputChk = globalDictInputChk, printSchema = False, verbose_func = globalVerbose, verbose = False):
		"""
		Return CSV output of self.dictout (default) or a similar dictionary object.
		Print this object's schema if asked to do so (default to no).
		"""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, tableSchema):
			allVals = None
			for key in tableSchema:
				allVals.append(dictInput[key])
			if len(allVals) == 13:
				if printSchema:
					return(genCSVfunc(tableSchema) + '\n' + genCSVfunc(allVals))
				else:
					return(genCSVfunc(allVals))
			else:
				# fail and return none if fewer than 13 output values found, as this is indicative of invalid input.
				raise ValueError(' : fewer than required number of output values found with standard global tableSchema on method CSVOut.  You are likely passing a miskeyed dictionary.')				
				return None
		else:
			return None
	def DictOut(self, dictInput = self.dictout, tableSchema = globalSchema, inputChk = globalDictInputChk, verbose_func = globalVerbose, verbose = False):
		"""Return a dictionary after validation."""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, tableSchema):
			return dictInput
		else:
			return None
	def TupleOut(self, dictInput = self.dictout, tableSchema = globalSchema, inputChk = globalDictInputChk, verbose_func = globalVerbose, verbose = False)
		"""Return a tuple based on a dictionary after validation, using provided tableSchema."""
		verbose_func(verbose, dictInput)
		if inputChk(dictInput, tableSchema):
			prelist = []
			for elem in tableSchema:
				prelist.append(dictInput[elem])
			return tuple(prelist)
		else:
			return None

class DSPerfDB:
	tableSchema = 'system_name', 
	def __init__(self, location=':memory:')
		self.con = sqlite3.connect(location)
		self.cur = self.con.cursor()
		# create table.
	def Close(self):
		self.con.close()