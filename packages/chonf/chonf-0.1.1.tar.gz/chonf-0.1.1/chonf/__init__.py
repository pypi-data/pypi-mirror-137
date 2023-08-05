"""
      _                  __ 
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  

Chooses configurations from multiple posible sources.

Functions:
    
    get(key, dir_path, *args, **kargs): Tries to get some user configuration

"""
from chonf.core import load, Option, Required, Repeat
from chonf.exceptions import ConfigReadingError, ConfigLoadingIncomplete, InvalidOption
from chonf.paths import default_path
