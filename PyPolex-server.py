#!/usr/bin/python 
"""
	PyPolex-Server
	Web Server Interface for image manipulations
"""

import cherrypy
import includes.ImageDownload as ImageDownload
import includes.ImageFile as ImageFile
import includes.ImageManipulation as ImageManipulation
from config import config

ID = ImageDownload.ImageDownload()
IF = ImageFile.ImageFile()
IM = ImageManipulation.ImageManipulation()

class Root( object ):

	def index( self, *args, **kwargs ):
		request_url = kwargs['url']
		img_args    = self.__arg_parser( kwargs )
		
		self.__check_cache_removal( img_args )
		self.__check_extra_args( img_args )
		cache = IF.loadByCache( request_url, img_args )
		if cache:
			content = cache
		else:
			image_path = ID.go( kwargs['url'], img_args )
			if image_path:
				im1      = IM.route( image_path, img_args )
				path     = IF.save( kwargs['url'], im1, img_args )
				content  = IF.loadByPath( path )
			else:
				return 'Error'
		cherrypy.response.headers['Content-Type'] = "image/jpg"
		return content
	index.exposed = True

	"""
		__arg_parser
		@description: Reads through arguments and builds out the proper request 
	"""
	def __arg_parser( self, args ):
		outbound = {}
		if 'crop' in args.iterkeys():
			dimension = args['crop'].split(',')
			outbound['crop'] = {}
			outbound['crop']['width']  = int( dimension[0] )
			outbound['crop']['height'] = int( dimension[1] )
		if 'watermark' in args.iterkeys():
			outbound['watermark'] = args['watermark']
		if 'flip' in args:
			outbound['flip'] = args['flip']
		return outbound

	"""
		__check_cache_removal
		@description: checks to see if 
	"""
	def __check_cache_removal( self, img_args ):
		if 'remove_cache' in img_args and img_args['remove_cache'] == True:
			cached_args = img_args
			cached_args.pop( 'remove_cache', None )
			IF.remove_cache( cached_args )

	def __check_extra_args( self, args ):
		if 'watermark' in args:
			image_path = ID.go( args['watermark'], { 'watermark' : True } )
			print ' '
			print ' '
			print ' '
			print 'watermark URL'
			print image_path
			print ''
			print ' '

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
