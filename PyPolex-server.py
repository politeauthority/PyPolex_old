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

	"""
		index
	"""
	def index( self, *args, **kwargs ):
		request_url = kwargs['url']
		img_args    = self.__arg_parser( kwargs )
		print kwargs
		print img_args
		self.__check_cache_removal( request_url, img_args )
		self.__check_extra_args( img_args )
		cache = IF.loadByCache( request_url, img_args )
		if cache:
			content = cache
		else:
			image_path = ID.go( kwargs['url'], img_args )
			if image_path:
				im1      = IM.get( image_path, img_args )
				path     = IF.save( kwargs['url'], im1, img_args )
				content  = IF.loadByPath( path )
			else:
				return 'Error'
		cherrypy.response.headers['Content-Type'] = "image/jpg"
		return content
	index.exposed = True

	"""
		documentation
		URL for resolving documentation
	"""
	def documentation( self ):
		return "Here's where I'll be putting documentation for this bad boy!"
	documentation.exposed = True

	"""
		__arg_parser
		@description: Reads through arguments and builds out the proper request 
	"""
	def __arg_parser( self, args ):
		outbound = {}
		if 'crop' in args:
			dimension = args['crop'].split(',')
			outbound['crop'] = {}
			outbound['crop']['width']  = int( dimension[0] )
			outbound['crop']['height'] = int( dimension[1] )
		if 'bg' in args:
			if len( args['bg'] ) == 6:
				outbound['bg'] = args['bg']
		if 'watermark' in args:
			outbound['watermark'] = args['watermark']
		if 'flip' in args:
			outbound['flip'] = args['flip']
		if 'matte' in args:
			outbound['matte']['size'] = args['matte']
			if 'matte_color' in args:
				outbound['matte']['color'] = args['matte_color']
		if 'clear_cache' in args:
			if args['clear_cache'] == 'True' or args['clear_cache'] == 'true':
				outbound['clear_cache'] = True
		return outbound

	"""
		__check_cache_removal
		@description: checks to see if a query should be removed
	"""
	def __check_cache_removal( self, request_url, img_args ):
		cached_args = img_args
		cached_args.pop( 'clear_cache', None )
		if 'clear_cache' in img_args and img_args['clear_cache'] == True:
			cached_args = img_args
			cached_args.pop( 'clear_cache', None )
			print ' '
			print ' '
			print ' '
			print request_url
			print cached_args
			IF.remove_cache( request_url, img_args )
			print ' '
			print ' '
			print ' '
			# IF.remove_cache( cached_args )

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

	def __handle_error( self, args ):
		return 'handle the error message here'

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
