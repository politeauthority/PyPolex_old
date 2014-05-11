#!/usr/bin/python
"""
  Image Download
  Checks the source of remote path, 
  checks the content vailidity,
  downloads and stores image
"""

import os
import sys
import urllib
import hashlib
import imghdr
sys.path.append( os.path.join(os.path.dirname(__file__), '../', '') )
from config import config
import includes.DriverLog as DriverLog

Log = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )

class ImageDownload( object ):

  def __init__( self ):
    self.remote_url = ''
    self.img_path   = ''

  def go( self, remote_url ):
    self.remote_url = remote_url
    self.__check_hosts()
    remote_image = urllib.urlopen( self.remote_url ).read()
    the_hash     = hashlib.md5( remote_url ).hexdigest()
    self.img_path     = config['upload_dir'] + the_hash
    f = open( self.img_path ,'wb')
    f.write( remote_image )
    f.close()
    Log.write( '    Saved File : %s' % self.img_path )  # Check Valid File Type
    self.__scan_file( )
    return self.img_path

  """
    Check Hosts
    Here we can run a white or black list filter on remote hosts
    that we wont accept connections from
  """
  def __check_hosts( self ):
    if self.remote_url in config['blacklist']:
      Log.write( '    Remote Host: %s is BANNED' % self.remote_url )
      return False
    else:
      return True

  """
    Check Valid File Type
  """
  def __scan_file( self ):
    valid_image_types = ['jpeg']
    if imghdr.what( self.img_path ) in valid_image_types:
      Log.write( '    Passed Extension Check : %s' % imghdr.what( self.img_path ) )
      return True
    else:
      Log.write( ' ERROR Failed Extension Check: %s ' % imghdr.what( self.img_path ) )
      sys.exit()
    return False