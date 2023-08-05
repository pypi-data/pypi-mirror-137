"""
      _                  __
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .parsers.env.core

Core functionality for the environment variable parser.

Functions:

    read(keys, *args, **kargs) -> str:
        Tries to read a configuration option from an environment variable.

"""
from typing import List, Set
import os, re

from chonf.exceptions import SkipSource, NotSubtree


def read(keys: List[str], env_prefix: str, *args, **kargs) -> str:
    """Tries to read a configuration option from an environment variable.

    Args:
        keys (List[str]): Sequence of keys to construct the env var name.
        env_prefix (str): Prefix of the env var name

    Returns:
        str: The env var value.

    Raises:
        SkipSource: For expected problems, to be ignored and skipped.

    """
    try:
        return os.environ["__".join([env_prefix, *keys])]
    except KeyError:
        raise SkipSource


def list_children(keys: List[str], env_prefix: str, *args, **kargs) -> Set[str]:
    parent_key = "__".join([env_prefix, *keys])
    children = set()
    for key, value in os.environ.items():
        if key == parent_key:
            raise NotSubtree(value)  # error when key is for a leaf node (not a dict)
        elif key.startswith(parent_key):
            child = re.split("__", key)[len(keys) + 1]
            children.add(child)
    return children
