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
		image_path = ID.go( kwargs['url'] )
		img_args = { 'crop': { 'width' : 600, 'height' : 600} }
		im1      = IM.route( image_path, img_args )
		path     = IF.save( kwargs['url'], im1 )
		content  = IF.loadByPath( path )
		cherrypy.response.headers['Content-Type'] = "image/jpg"
		return content
	index.exposed = True

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
