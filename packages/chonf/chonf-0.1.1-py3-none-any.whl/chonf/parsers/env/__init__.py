"""
      _                  __
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .core.parsers.env

Provides access to environment variables.

To support nested configs on env vars, chonf provides
a special syntax, consider a python dict that might
be accessed this way:

myconfs['section2']['option8']

A nested structure like this is not supported by env
vars. With chonf you can define this configuration
option by joining the sequence of keys with "__",
adding a prefix to identify the program and isolate
it from other programs:

python:  >>> os.environ['myprogram__section2__option8'] = "value"

posix:   $ myprogram_section2__option8 = "value"

fish:    > set -x myprogram_section2__subsect4__option8 "value"

Then, a program can read this configuration by passing
a list of keys as usual with chonf, passing the program 
prefix in the env_prefix argument:

python:  >>> chonf.get(['section2', 'subsect4', 'option8'], 
         ...           env_prefix='myapp')

The chonf.get() function calls the read() config from each parser
module in chonf.core.parsers until it finds something valid,
The environment variable parser is the first, so it can be used
to quickly short-circuit other configuration sources for quick
tests.

Functions:

    read(keys, *args, **kargs) -> str:
        Tries to read an environment variable, return missing if failed.

"""
from chonf.parsers.env.core import read, list_children
