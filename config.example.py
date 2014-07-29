#!/usr/bin/python
"""
  PyPollex Config File
  rename file to config.py before use
"""
config = {
  'verbosity'     : True,
  'use_cache'     : True,
  'app_dir'       : '/home/alix/Repos/PyPolex/',
  'img_dir'       : '/home/alix/Repos/PyPolex/images/',
  'log_dir'       : '/home/alix/Repos/PyPolex/logs/',
  'whitelist'     : [ 'vailrealestate.com' ],
  'blacklist'     : [ 'imgur.com', 'flickr.com' ],
  'webserver'     : {
    'global': {
      'server.socket_port'          : 9000,
      'server.socket_host'          : "192.168.7.70",
      'server.socket_file'          : "",
      'server.socket_queue_size'    : 5,
      'server.protocol_version'     : "HTTP/1.0",
      'server.log_to_screen'        : True,
      'server.log_file'             : "logs/server.log",
      'server.reverse_dns'          : False,
      'server.thread_pool'          : 40,
      'server.environment'          : "development",
    },
  }
}

# End File: config.py
