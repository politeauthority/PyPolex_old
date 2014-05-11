#!/usr/bin/python                                                                                                
# Log Driver
# This driver helps write quick log files

import datetime
import time
class DriverLog( object ):

	def __init__( self, phile, verbosity = False ):
		self.phile_name = phile
		self.verbosity  =  verbosity

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
# End File: DriverLog.py
