"""
  PyPolix config
  rename file to config.py before use
"""
config = {
  'verbosity'     : True,
  'use_cache'     : True,
  'upload_dir'    : '/home/user/PyPollex/images/uploads/',
  'cache_dir'     : '/home/user/PyPollex/images/cache/',
  'log_dir'       : '/home/user/PyPollex/PyThumbs/logs/',
  'use_whitelist' : False,
  'whitelist'     : [],
  'use_blacklist' : False,
  'blacklist'  : [
    'imgur.com',
    'flickr.com'
  ],
  'webserver'     : {
      'global': {
        'server.socket_port'          : 8099,
        'server.socket_host'          : "10.1.10.55",
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

# End File: config.example.py
