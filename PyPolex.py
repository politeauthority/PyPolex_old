#!/usr/bin/python
"""
  PyPolex
  Image Modification Tool
"""

import sys
import os
import includes.DriverLog as DriverLog
import includes.ImageDownload as ImageDownload
import includes.ImageFile as ImageFile
import includes.ImageManipulation as ImageManipulation
from config import config

ID = ImageDownload.ImageDownload()
IF = ImageFile.ImageFile()
IM = ImageManipulation.ImageManipulation()

Log = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )

def check_for_cache( url_request ):
  Log.write( '  Checking Cache ' )
  if config['ignore_cache']:
    return False
  the_hash = hashlib.md5( url_request ).hexdigest()
  cache_location = cache_dir + the_hash + ".jpg"
  if os.path.isfile( cache_location ):
    Log.write( '    Cache Found: %s' % cache_location )
    return cache_location
  else:
    Log.write( '    Cache Not Found')
    return False

if __name__ == "__main__":
  Log.write( '' )
  Log.write( '' )  
  Log.write( 'New Request' )
  url = sys.argv[1]
  img_cache = check_for_cache( url )
  if img_cache:
    sys.exit()
  Log.write( '  Downloading : %s' % url )
  local_image_path = ImageDownload.ImageDownload().go( url )

  args = {
    'crop': { 'width' : 200, 'height' : 200}
  }

  im1 = ImageManipulation.ImageManipulation().route( local_image_path, args )

  IF.save( url, im1 )
  Log.write( 'Finished' )

# End File: PyPolex.py
