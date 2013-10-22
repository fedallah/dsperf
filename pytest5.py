#!/usr/bin/env python3

import sqlite3
from datetime import datetime
import re

class InputFile:
	rm_trailcomma = re.compile(',{1}$|,{1}\n')
	def __init__(self, path):
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
	def Dump():
		try:
			for line in open(self.path):
				if ( len(line) > 0 ) and ( line.count(',') == 12 ):
					line = re.sub(rm_trailcomma,'',line)
					yield line	# return a generator object!
				else:
					continue
		except:
			raise IOError(' : could not open file on class InputFile for method \'Dump\' at location \"' + str(self.path) + '\".  Aborting.')
			return None

class PerfObj:
	get_controller = re.compile(',CONTROLLER IN SLOT (\w{1}),')
	get_LD = re.compile(',Logical Drive (.*?),')
	def __init__(self, u_input, verbose=False):
		lu_input = u_input.split(',', 11)
		self.dictout = {}
		if verbose:
			print('VERBOSE: Input on PerfObj constructor is: ' + str(u_input) + ' : .')
		if len(lu_input) == 12:
			self.dictout['system_name'] = str(u_input[0])
			self.dictout['timestamp'] = datetime.strptime(lu_input[1])
			self.dictout['IPaddr_controllerA'] = str(u_input[2])
			self.dictout['IPaddr_controllerB'] = str(u_input[3])		
			if ( get_controller.search(u_input[4]) ) and ( get_LD.search(u_input[4]) ):
				raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\' - both controller and logical drive found where only one expected')
			elif get_controller.search(u_input[4]):
				self.dictout['controllerTotal'] = get_controller.search(inp).group(1)
				self.dictout['LogicalDriveName'] = None
			elif get_LD.search(u_input[4]):
				self.dictout['controllerTotal'] = None
				self.dictout['LogicalDriveName'] = get_LD.search(inp).group(1)
			else:
				raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\'')
				return None
			self.dictout['total_IOPS'] = int(u_input[5])
			self.dictout['read_percent'] = float(u_input[6])
			self.dictout['cache-hit_percent'] = float(u_input[7])
			self.dictout['current_KBsec'] = float(u_input[8])
			self.dictout['max_KBsec'] = float(u_input[9])
			self.dictout['current_IOPS'] = float(u_input[10])
			self.dictout['max_IOPS'] = float(u_input[11])
			if verbose:
				print('VERBOSE: Output on PerfObj constructor is: ' + str(dictout) + ' : .')
			return self.dictout
		else:
			raise AttributeError(' : Found ' + str(len(lu_input)) + ' fields in input string:\n' + u_input + '\n... where 12 expected on class \'PerfObj\', constructor method.  Invalid input.')
			return None
	def SingleDBInsert:

class PerfGroup:
	def __init__(self, whichdb):
		if len(self.output) == 0:
			self.output = ()
			return True
		else:
			raise "Warning: calling constructor on non-empty object from class PerfGroup.  No values have been added or removed."
			return False
	def Add(dict_in):
		if isinstance(dict_in, dict):
			
		else:
			raise ValueError(' : invalid input - method \'Add\' on class PerfGroup expects input as dictionary')
	def DeDup:
		if len(self.output > 0):
			
		else:
			raise ValueError(' : nothing to deduplicate')
	def MkCSV:
		if len(self.output > 0):
		
		else:
			raise ValueError(' : nothing to output.')
	def DBInsert: