import sys
import os
import urllib
import imghdr
import Image
import hashlib
import DriverLog

verbosity    = True
upload_dir   = '/home/alix/Dropbox/PyThumbs/uploads/'
cache_dir    = './cache/'
ignore_cache = True
log_dir      = '/home/alix/Dropbox/PyThumbs/logs/'
Log          = DriverLog.DriverLog( log_dir + 'new_log', True )

class DownloadImage( object ):

  def __init__( self ):
    self.remote_url = ''

  def go( self, remote_url ):
    self.remote_url = remote_url
    remote_image = urllib.urlopen( self.remote_url ).read()
    the_hash     = hashlib.md5( get_url ).hexdigest()
    img_path     = upload_dir + the_hash
    f = open( img_path,'wb')
    f.write( remote_image )
    f.close()
    Log.write( '    Saved File : %s' % img_path )  # Check Valid File Type
    self.__scan_file( )
    return img_path

  """
    Check Hosts
    Here we can run a white or black list filter on remote hosts
    that we wont accept connections from
  """
  def __check_hosts( ):
    print 'check if the hosts are cool'

  """
    Check Valid File Type
  """
  def __scan_file( self ):
    valid_image_types = ['jpeg']
    if imghdr.what( img_path ) in valid_image_types:
      Log.write( '    Passed Extension Check : %s' % imghdr.what( img_path ) )
    else:
      Log.write( ' ERROR Failed Extension Check: %s ' % imghdr.what( img_path ) )
      sys.exit()
    return img_path



def getImageByUrl( get_url ):
  remote_image = urllib.urlopen( get_url ).read()
  the_hash     = hashlib.md5( get_url ).hexdigest()
  img_path     = upload_dir + the_hash
  f = open( img_path,'wb')
  f.write( remote_image )
  f.close()
  Log.write( '    Saved File : %s' % img_path )  # Check Valid File Type

  # Check Valid File Type
  valid_image_types = ['jpeg']
  if imghdr.what( img_path ) in valid_image_types:
    Log.write( '    Passed Extension Check : %s' % imghdr.what( img_path ) )
  else:
    Log.write( ' ERROR Failed Extension Check: %s ' % imghdr.what( img_path ) )
    sys.exit()
  return img_path

  # print remote_image

def imgResize( local_image_path, args ):
  Log.write( '  Image Resizing' )
  Log.write( '    Args: %s' % args )
  d_width  = args['crop']['width']
  d_height = args['crop']['height']
  im = Image.open( local_image_path )
  # Prepare to resize the image
  o_width  = im.size[0] 
  o_height = im.size[1]
  Log.write( '    Original Width: %spx, Original Height: %spx' % ( o_width, o_height ) )    
  if d_width < d_height:
    d_smaller = d_width
  else:
    d_smaller = d_height

  if o_width < o_height:
    o_smaller = o_width
  else:
    o_smaller = o_height
  divisor = 2  
  while True:
    result = o_smaller / divisor
    if result < d_smaller:
      divisor = divisor - 1
      break
    divisor = divisor + 1

  n_width  = o_width / divisor
  n_height = o_height / divisor
  Log.write( '    Scaled Width: %spx, Scaled Height: %spx' % ( n_width, n_height ) ) 
  # Prepare the Crop
  if n_width > n_height:
    crop_left  = ( n_width / 2 ) - ( d_width / 2 )
    crop_upper = 0
    crop_right = crop_left + d_width 
    crop_lower = d_height
  else:
    crop_left  = 0
    crop_upper = ( n_height / 2 ) - ( d_width / 2 )
    crop_right = d_width
    crop_lower = crop_upper + d_width

  crop_cords = ( crop_left, crop_upper, crop_right, crop_lower )
  Log.write( '    Crop Cords: Left %spx, Upper: %spx, Right: %s, Lower: %s' % ( crop_left, crop_upper, crop_right, crop_lower ) )    
  im = im.resize((n_width, n_height), Image.ANTIALIAS) # best down-sizing filter
  im = im.crop( crop_cords )
  return im

def imgSave( raw_request, im ):
  the_hash = hashlib.md5( raw_request ).hexdigest()
  prepared_image = cache_dir + the_hash + ".jpg"
  im.save( prepared_image )
  Log.write( '    Saved Image: ' + prepared_image )\

def check_for_cache( url_request ):
  Log.write( '  Checking Cache ' )
  if ignore_cache:
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
  local_image_path = getImageByUrl( url )

  args = {
    'crop': { 'width' : 200, 'height' : 200}
  }

  # Log.write('  Using Args :')

  im1 = imgResize( local_image_path, args )

  imgSave( url, im1 )
  Log.write( 'Finished' )

