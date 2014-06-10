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
    self.img_path   = False

  """
    Go
    Kicks off the entire download process
    @params: remote_url str() remote image url to download
  """
  def go( self, remote_url, args = None ):
    Log.write( '  Downloading: %s' % remote_url )
    self.remote_url = remote_url
    if not self.__check_hosts():
      return False
    remote_image    = urllib.urlopen( self.remote_url ).read()
    the_hash        = hashlib.md5( remote_url ).hexdigest()
    if 'watermark' in args:
      self.img_path   = config['img_dir'] + 'watermark/' + the_hash
    else:
      self.img_path   = config['upload_dir'] + the_hash
    f = open( self.img_path ,'wb')
    f.write( remote_image )
    f.close()
    Log.write( '    Saved File : %s' % self.img_path )  # Check Valid File Type
    if not self.__scan_file():
      return False
    return self.img_path

  """
    __check_hosts
    Here we can run a white or black list filter on remote hosts
    that we wont accept connections from
  """
  def __check_hosts( self ):
    if config['use_whitelist']:
      print 'Using White List'
    if config['use_blacklist']:
      if self.remote_url in config['blacklist']:
        Log.write( '    Remote Host: %s is BANNED' % self.remote_url )
        return False
    return True

  """
    __scan_file
    @description: Check if we have a valid image File
    @todo: Is not curently working
  """
  def __scan_file( self ):
    valid_image_types = [ 'jpeg', 'jpg' ]
    print ' '
    print ' '
    print ' '
    print imghdr.what( self.img_path )
    print ' '
    print ' '
    print ' '
    return True
    if imghdr.what( self.img_path ) in valid_image_types:
      Log.write( '    Passed Extension Check : %s' % imghdr.what( self.img_path ) )
      return True
    else:
      Log.write( ' ERROR Failed Extension Check: %s ' % imghdr.what( self.img_path ) )
    return False

# End File: includes/ImageDownload.py

