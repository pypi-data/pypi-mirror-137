"""
      _                  __ 
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .core

Provides the core functionality for chonf.

Functions:

    load(model, env_prefix, dir_path): returns a dictionary constructed based
        on the provided model of configurations, with data read from several
        sources.

Classes:

    Option(default): to be used to create model dictionary to be passed on
        to the load function.

"""
from typing import List, Tuple, Any, Union, Optional, Callable
from functools import partial
from dataclasses import dataclass
from pathlib import Path
from os import PathLike

from chonf.parsers import default_parsers
from chonf.exceptions import (
    NotSubtree,
    SkipSource,
    ConfigReadingError,
    ConfigNotFound,
    ConfigLoadingIncomplete,
    InvalidOption,
)
from chonf.paths import default_path


class BaseOption:
    """Base class for chonf options."""


@dataclass
class Option(BaseOption):
    """Dataclass to represent a config value to be read."""

    default: Any = None
    pre_process: Optional[Callable[[Any], Tuple[bool, Any]]] = None


@dataclass
class Required(BaseOption):
    """Class to represent a required config value to be read."""

    pre_process: Optional[Callable[[Any], Tuple[bool, Any]]] = None


@dataclass
class Repeat(BaseOption):
    """Defines a repeatable substructure within the config model
    with arbitrary root keys."""

    submodel: Union[BaseOption, dict]


@dataclass
class Invalid:
    value: Any
    expected: Any


def load(
    model: dict,
    author: str,
    name: str,
    env_prefix: str = None,
    path: Union[PathLike, str, List[Union[PathLike, str]]] = None,
    *args,
    **kargs,
) -> dict:
    """Load configurations from multiple sources based on
    a model defined as a dictionary.
    """
    if path is None:
        path = default_path(author, name)
    if env_prefix is None:
        env_prefix = name
    if not isinstance(path, list):
        path = [path]

    _search_config = partial(
        search_config, env_prefix=env_prefix, path=path, *args, **kargs
    )

    _repeat_subtree = partial(
        repeat_subtree, env_prefix=env_prefix, path=path, *args, **kargs
    )

    unlocated_keys = []
    invalid_keys = []
    expected_subtree_keys = []

    def _recurse(model, parent_keys=[]):
        configs = {}
        for key, value in model.items():
            keys = parent_keys + [key]
            if isinstance(value, dict):
                config = _recurse(value, keys)
            elif isinstance(value, Option):
                try:
                    config = _search_config(keys, pre_process=value.pre_process)
                except ConfigNotFound:
                    config = value.default
                except InvalidOption as inv_opt:
                    config = inv_opt
                    invalid_keys.append(keys)
            elif isinstance(value, Required):
                try:
                    config = _search_config(keys, pre_process=value.pre_process)
                except ConfigNotFound:
                    config = InvalidOption(None, value)
                    unlocated_keys.append(keys)
                except InvalidOption as inv_opt:
                    config = inv_opt
                    invalid_keys.append(keys)
            elif isinstance(value, Repeat):
                try:
                    config = _recurse(_repeat_subtree(keys, value), keys)
                except InvalidOption as inv_opt:
                    config = inv_opt
                    expected_subtree_keys.append(keys)
            else:
                config = value
            configs[key] = config
        return configs

    configs = _recurse(model)

    if (
        len(unlocated_keys) != 0
        or len(invalid_keys) != 0
        or len(expected_subtree_keys) != 0
    ):
        raise ConfigLoadingIncomplete(
            unlocated_keys, invalid_keys, expected_subtree_keys, configs
        )

    return configs


def search_config(
    keys: List[str],
    env_prefix: str = "",
    path: List[Union[PathLike, str]] = "",
    parsers=default_parsers,
    pre_process: Optional[Callable[[Any], Any]] = None,
    *args,
    **kargs,
) -> Any:
    """Search a configuration variable from multiple sources."""

    if pre_process is None:
        pre_process = lambda x: x
    for p in path:
        p = Path(p)
        for parser in parsers:
            try:
                value = pre_process(
                    parser.read(
                        keys=keys, path=p, env_prefix=env_prefix, *args, **kargs
                    )
                )
                return value
            except SkipSource:
                continue
            except InvalidOption:
                raise
            except Exception as err:
                raise ConfigReadingError from err
    else:
        raise ConfigNotFound


def repeat_subtree(
    keys: List[str],
    repeat: Repeat,
    env_prefix: str = "",
    path: List[Union[PathLike, str]] = "",
    parsers=default_parsers,
    *args,
    **kargs,
) -> dict:
    """Compose repetition of configuration submodel."""
    root_keys = set()
    for p in path:
        p = Path(p)
        for parser in parsers:  # try to get all existing child keys
            try:
                root_keys.update(
                    parser.list_children(
                        keys=keys, path=p, env_prefix=env_prefix, *args, **kargs
                    )
                )
            except NotSubtree as not_subtree:
                raise InvalidOption(not_subtree.value, repeat)
            except Exception as err:
                raise ConfigReadingError from err
    return {key: repeat.submodel for key in root_keys}
