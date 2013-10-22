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
					yield line
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
		dictout = {}
		if verbose:
			print('VERBOSE: Input on PerfObj constructor is: ' + str(u_input) + ' : .')
		if len(lu_input) == 12:
			dictout['system_name'] = str(u_input[0])
			dictout['timestamp'] = datetime.strptime(lu_input[1])
			dictout['IPaddr_controllerA'] = str(u_input[2])
			dictout['IPaddr_controllerB'] = str(u_input[3])		
			if get_controller.search(u_input[4]):
				dictout['controllerTotal'] = get_controller.search(inp).group(1)
				dictout['LogicalDriveName'] = None
			elif get_LD.search(u_input[4]):
				dictout['controllerTotal'] = None
				dictout['LogicalDriveName'] = get_LD.search(inp).group(1)
			else:
				raise ValueError(' : unexpected input of ' + str(u_input[4]) + ' for controller or logical drive field #5 to constructor on class \'PerfObj\'')
			dictout['total_IOPS'] = int(u_input[5])
			dictout['read_percent'] = float(u_input[6])
			dictout['cache-hit_percent'] = float(u_input[7])
			dictout['current_KBsec'] = float(u_input[8])
			dictout['max_KBsec'] = float(u_input[9])
			dictout['current_IOPS'] = float(u_input[10])
			dictout['max_IOPS'] = float(u_input[11])
			if verbose:
				print('VERBOSE: Output on PerfObj constructor is: ' + str(dictout) + ' : .')
			return dictout
		else:
			raise AttributeError(' : Found ' + str(len(lu_input)) + ' fields in input string:\n' + u_input + '\n... where 12 expected on class \'PerfObj\', constructor method.  Invalid input.')