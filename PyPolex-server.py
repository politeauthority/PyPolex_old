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
		
		cache = IF.loadByCache( request_url, img_args )
		if cache:
			content = cache
			print 'loaded by cache'
			print 'loaded by cache'
			print 'loaded by cache'
			print 'loaded by cache'
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

	def __arg_parser( self, args ):
		outbound = {}
		if 'crop' in args.iterkeys():
			dimension = args['crop'].split(',')
			outbound['crop'] = {}
			outbound['crop']['width']  = int( dimension[0] )
			outbound['crop']['height'] = int( dimension[1] )
		return outbound

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
