#!/usr/bin/python 
"""
	PyPolex-Server
	Web Server Interface for image manipulations
"""

import cherrypy
from config import config
import includes.ImageDownload as ImageDownload
import includes.ImageFile as ImageFile
import includes.ImageManipulation as ImageManipulation
import includes.DriverRenderer as DriverRenderer

ID = ImageDownload.ImageDownload()
IF = ImageFile.ImageFile()
IM = ImageManipulation.ImageManipulation()
Render = DriverRenderer.DriverRenderer()

class Root( object ):

	def index( self, *args, **kwargs ):
		"""
			Main site index

		"""
		if 'url' not in kwargs:
			return self.__handle_error( { 'msg': '', 'view': 'no_args' } )
		request_url = kwargs['url']
		img_args    = self.__arg_parser( kwargs )
		print ' '
		print ' '
		print ' '
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
			# else:
			# 	return self.__handle_error( { 'msg' : 'Error in Downloading' } )
		cherrypy.response.headers['Content-Type'] = "image/jpg"
		return content
	index.exposed = True

	def documentation( self ):
		"""
			URL for resolving documentation
		"""
		return "Here's where I'll be putting documentation for this bad boy!"
	documentation.exposed = True

	def __arg_parser( self, args ):
		"""
			Reads through arguments and builds out the proper request 
		"""
		outbound = {}
		if 'crop' in args:
			dimension = args['crop'].split(',')
			outbound['crop']           = {}
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

	def __check_cache_removal( self, request_url, img_args ):
		"""
			Checks to see if a cache should be removed
		"""
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

	def __handle_error( self, error ):
		if 'data' in error:
			data = {}
		else:
				data = error['msg']
		if 'view' in error:
			return Render.make( str( 'error/' + error['view'] ), data )
		else:
			return 'handle the error message here'

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
