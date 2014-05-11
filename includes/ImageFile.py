#!/usr/bin/python
"""
  Image File
  Handlers for file interactions.
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '../', '') )
from config import config
import includes.DriverLog as DriverLog

Log = DriverLog.DriverLog( config['log_dir'] + 'new_log', config['verbosity'] )

class ImageFile( object ):

  def __init__( self ):
    self.phile_path = ''

  def save( self, phile_path ):
    self.phile_path = phile_path

# End File: includes/ImageFile.py
