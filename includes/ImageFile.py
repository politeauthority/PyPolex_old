#!/usr/bin/python
"""
  Image File
  Handlers for file interactions.
"""

import sys
import os
import hashlib
sys.path.append( os.path.join(os.path.dirname(__file__), '../', '') )
from config import config
import includes.DriverLog as DriverLog

Log = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )

class ImageFile( object ):

	def __init__( self ):
		self.cache_dir  = config['cache_dir']
		self.phile_path = ''

	"""
		Save
		@params:
			url : str()
			img : object( image )
	"""
	def save( self, url, img ):
		the_hash = hashlib.md5( url ).hexdigest()
		self.phile_path = config['cache_dir'] + the_hash + '.jpg'
		img.save( self.phile_path )
		# img.save( self.phile_path )
		Log.write( '    Saved Image: ' + self.phile_path )
		return self.phile_path

	"""
		loadByPath
	"""
	def loadByPath( self, path ):
		f = open( path, 'rb' )
		contents = f.read()
		f.close
		# print contents
		return contents

	"""
		loadByUrl
	"""
	def loadByUrl( self, url ):
		the_hash = hashlib.md5( url ).hexdigest()
		f.open( self.cache_dir + the_hash + '.jpg' )
		f.close
		return f

# End File: includes/ImageFile.py
