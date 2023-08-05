"""
      _                  __ 
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  core.parsers

Modules to parse different kinds of configurations.

"""
from chonf.parsers import env, toml, json

default_parsers = [env, toml, json]
