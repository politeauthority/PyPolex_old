#!/usr/bin/python
"""
	Log Driver
	This is just a basic driver for write quick log files
	example commands for log reading:
		less logs/run_log.txt | grep 'downloaded'
		tail -f logs/run_log.txt | grep 'downloaded'
	@author: Alix Fullerton
"""

import os
import datetime

class DriverLog( object ):

	def __init__( self, phile, verbosity = False ):
		self.phile_name = phile
		self.verbosity  =  verbosity
		self.__create_blank()

	def write( self, line ):
		time = ''
		if line != '':
			the_time = datetime.datetime.now()
			line = "[%s] %s" % ( str(the_time), str( line ) )
		if self.verbosity:
			print line
		self.line_prepender( self.phile_name, line )
		return True

	def line_prepender( self, filename, line ):
		with open( filename,'r+') as f:
			content = f.read()
			f.seek(0,0)
			f.write(line.rstrip('\r\n') + '\n' + content)

	def __create_blank( self ):
		if not os.path.isfile( self.phile_name ):
			f = open( self.phile_name,'w')
			f.write('\n')
			f.close()

# End File: DriverLog.py
