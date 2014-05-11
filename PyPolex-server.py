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
		img_args = { 'crop': { 'width' : 200, 'height' : 200} }
		im1 = IM.route( image_path, img_args )
		path = IF.save( kwargs['url'], im1 )
		path = ''
		self.show_img( path )
		# return str(args ) + ' ' + str( kwargs ) + ' ' + path
	index.exposed = True

	def show_img( self, path ):
		cherrypy.response.headers['Content-Type'] = "image/jpg"
		# f = open( path, 'rb' )
		f = open( '/home/alix/Dropbox/Python-Fun/PyPollex/cache/a627336a5ed9c0f4295b9a77f53abc60.jpg', 'rb' )
		contents = f.read()
		f.close()
		return contents
		# return IF.loadByPath( path )

if __name__ == '__main__':  
  cherrypy.quickstart( Root(),  config = config['webserver'] )

# End File: PyPolex-server.py
