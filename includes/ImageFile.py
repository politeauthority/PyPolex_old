#!/usr/bin/python
"""
  Image File
  Handlers for file interactions.
"""

import os
import hashlib
from config import config
import DriverMysql as DriverMysql
import DriverLog as DriverLog

Log   = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )
Mysql = DriverMysql.DriverMysql( config['database'] )

class ImageFile( object ):

	def __init__( self ):
		self.cache_dir  = config['img_dir'] + 'cache/'
		self.upload_dir = config['img_dir'] + 'uploads/'
		self.phile_path = ''

	"""
		Save
		@params:
			url : str()
			img : object( image )
	"""
	def save( self, url, img, args ):
		the_hash = hashlib.md5( url + str( args ) ).hexdigest()
		self.phile_path = self.cache_dir + the_hash + '.jpg'
		img.save( self.phile_path )
		self.__insert( url )
		Log.write( '    Saved Image: ' + self.phile_path )
		return self.phile_path

	"""
		loadByPath
	"""
	def loadByPath( self, path ):
		f = open( path, 'rb' )
		contents = f.read()
		f.close
		return contents

	"""
		loadByUrl
	"""
	def loadByUrl( self, url ):
		the_hash = hashlib.md5( url ).hexdigest()
		f.open( self.cache_dir + the_hash + '.jpg' )
		f.close
		return f

	"""
		loadByCahce
		@params:
			url  : str( )
			args : dict{ }
	"""
	def loadByCache( self, url, args ):
		if config['use_cache']:
			the_hash = hashlib.md5( url + str( args ) ).hexdigest()
			self.phile_path = self.cache_dir + the_hash + '.jpg'
			if os.path.isfile( self.phile_path ):
				return self.loadByPath( self.phile_path )
		return False

	"""
		removeCache
		@description: destroys caches on request
		@todo
			- rate limit this so bots dont end up creating issues
			- also, MAKE THIS WORK!
	"""
	def removeCache( self, url, args ):
		print 'here we should be removing caches!'
		the_hash = hashlib.md5( url + str( args ) ).hexdigest()
		print the_hash
		print self.cache_dir

	"""
		__insert
	"""
	def __insert( self, url ):
		params = { 
			'database' : config['database'], 
			'path'     : self.phile_path,
			'url'      : url, 
		}
		qry = """INSERT INTO `%(database)s`.`images` 
			( `path`, `url` )  
			VALUES (  "%(path)s", "%(url)s" );""" % params
		print qry
		# Mysql.conn()
		# Mysql.ex( qry )
		# Mysql.close()

# End File: includes/ImageFile.py
