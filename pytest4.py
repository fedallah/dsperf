#!/usr/bin/env python3

import sqlite3
from datetime import datetime

class InputFile:
	def __init__(self, path):
		self.path = path
		try:
			with open(self.path) as ifile:
				first_val = ifile.readline()
				isval = first_val.count(',')
				if ( len(isval) != 12 ):
					raise AttributeError(' : Found ' + str(len(isval)) + ' fields in first line of input file at ' + self.path + ' where 12 expected.  This does not look like a valid file.')
		except IOError:
			print('Could not open file on class InputFile for constructor method at location ' + str(self.path) + '.  Aborting.')
			return False
	def Dump():
		try:
			with open(self.path) as ifile:
				for line in ifile:
					return line	
		except IOError:
			print('Could not open file on class InputFile for method \'Dump\' at location ' + str(self.path) + '.  Aborting.')
			return False
				
class PerfObj:
	def __init__(self, u_input, verbose=False):
		lu_input = u_input.split(',', 11)
		if ( verbose is True ):
			print('Input on PerfObj constructor is: ' + str(u_input) + '.')
		if ( len(lu_input) == 12 ):
			ic = 0			
			while ic < 12:
				if ( ic == 0 ):
					output['system_id'] = str(lu_input[ic])
				elif ( ic == 1 ):
					output['timestamp'] = datetime.strptime(lu_input[ic], '%m/%d/%Y %X')
				elif ( ic == 2 ):
					output['IPaddr_controllerA'] = str(lu_input[ic])
				elif ( ic == 3 ):
					output['IPaddr_controllerB'] = str(lu_input[ic])
				elif ( ic == 4 ):
					if ( (lu_input[ic].count('CONTROLLER') > 0 ):
						cont_total = lu_input[ic].split(' ', 1)
						output['Controller_Total'] = 
			
				if ( ic == 0 ) or ( ic > 1 and ic < 5 ):
					try:
						rawout[ic] = str(lu_input[ic])
					except AttributeError:
						print('Failed to cast value as string on class \'PerfObj\', method \'Ingest\'.  Invalid input.')
						return False
						break
				elif ( ic == 5 ):
					try:
						rawout[ic] = int(lu_input[ic])
					except AttributeError:
						print('Failed to cast input ' + str(lu_input[ic]) + ' as integer where integer expected on class \'PerfObj\', method \'Ingest\'.  Invalid input.')
						return False
						break
				elif ( ic > 5 ):
					try:
						rawout[ic] = float(lu_input[ic])
					except AttributeError:
						print('Failed to cast input ' + str(lu_input[ic]) + ' as float where float expected on class \'PerfObj\', method \'Ingest\'.  Invalid input.')
						return False
						break
				ic += 1
			return output
		else:
			raise AttributeError(' : Found ' + str(len(lu_input)) + ' fields in input string:\n' + u_input + '\n... where 12 expected on class \'PerfObj\', method \'Ingest\'.  Invalid input.')
			return False
	def DBInsert(db_in):

class PerfGroup:
	def __init__(self)
		self.output = ()
		return self.output
	def DBBulkInsert:
		for el in self.output:
		
class PerfPoint: