"""
      _                  __
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .parsers.json.core

Core functionality for chonf's json configuration parser.

Functions:

    read(keys: List[str], dir_path: pathlib.Path, *args, **kargs) -> Any: 
        Tries to read a configuration option from a json file. 

"""
from functools import cache
from typing import List, Any
from pathlib import Path
import json

from chonf.exceptions import FileAccessError, NotSubtree, SkipSource, InvalidOption


def read(keys: List[str], path: Path, *args, **kwargs) -> Any:
    """Tries to read a configuration option from a Json file.

    Args:
        keys (List[str]): Ordered keys to access the option.
        dir_path: (pathlib.Path): path object representing the file

    Returns:
        Any: Whatever data is found in the file with the given keys.
    """
    config = load_configs(path / "config.json")
    try:
        for key in keys:
            config = config[key]
    except KeyError:
        raise SkipSource
    return config


def list_children(keys: List[str], path: Path, *args, **kwargs) -> Any:
    """Tries to list all children of a configuration node on a Json file.

    Args:
        keys (List[str]): Ordered keys to access the node.
        dir_path: (pathlib.Path): path object representing the file

    Returns:
        Set[str]: list of children keys to requested node, might be empty.

    """
    config = load_configs(path / "config.json")
    try:
        for key in keys:
            config = config[key]
    except KeyError:
        return set()
    if isinstance(config, dict):
        return set(config.keys())
    else:
        raise NotSubtree(config)


@cache
def load_configs(path: Path) -> dict:
    """Reads a Json file into a dict.

    This wraps the load() function from the json package,
    and will use it's default behaviour when called with
    only a file object created by open(path).

    Args:
        path (pathlib.Path): Path to the json file.

    Returns:
        dict: Data read from json file.
    """
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}
    except Exception as err:
        raise FileAccessError from err
