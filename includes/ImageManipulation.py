#!/usr/bin/python
"""
  Image Manipulation
  Assortment of image adjustment methods
"""

import sys
import os
import Image
sys.path.append( os.path.join(os.path.dirname(__file__), '../', '') )
from config import config
import includes.DriverLog as DriverLog

Log = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )

class ImageManipulation( object ):

  def __init__( self ):
    self.local_path = ''
    self.img        = ''
    self.args       = ''

  def route( self, local_path, args ):
    Log.write( '  Image Resizing' )
    Log.write( '    Args: %s' % str( args ) )      
    self.local_path = local_path
    self.args       = args
    for key, value in self.args.iteritems():
      if key == 'crop':
        self.img = self.crop()
      elif key == 'maxWidth' or key == 'maxHeight':
        self.img = self.maxSize( dimension = key )
    return self.img

  def resize( self, extra_args = None ):
    print 'max width of height here'

  def crop( self, extra_args = None ):
    d_width  = self.args['crop']['width']
    d_height = self.args['crop']['height']
    im = Image.open( self.local_path )
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

  def wattermark( self ):
    print 'wattermarkign'

  def mirror( self ):
    print 'mirror'

  def maxSize( self, dimension ):
    print 'force either width or height to be a max size'
    if dimension == 'width':
      print 'the max width is ', self.args['maxWidth']
    elif dimension == 'height':
      print 'the max height is', self.args['maxHeight']

# End File: includes/ImageManipulation.py
