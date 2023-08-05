"""
      _                  __ 
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .core.exceptions

Provides exceptions for chonf.

Classes (exceptions):

    ConfigReadingError: Raised when an attempt to read a configuration fails
        in an unexpected manner.

    FileAccessError: Raised when an attempt to access a config file fails
        in an unexpected manner.

    SkipSource: Raised when an attempt to access a config source fails in an
        expected manner, so that chonf can continue looking elsewhere.

"""


from dataclasses import dataclass
from typing import List, Any


class ConfigReadingError(Exception):
    """Throw when an attempt to access a configuration option fails
    in an unexpected manner, for a more comprehensive error log.
    """

    pass


class FileAccessError(Exception):
    """Throw when an attempt to read a configuration file fails in an
    unexpected manner, for a more comprehensive error log.

    Should not be confused with FileNotFoundError, as this exception
    is expected and should usually cause a SkipSource exception to
    be raised.
    """

    pass


class SkipSource(Exception):
    """Throw when an attempt to access a configuration source fails
    in an expected way, to signify the getter to continue looking at
    other sources without stopping the program.
    """

    pass


class ConfigNotFound(Exception):
    """Throw when an attempt to find a configuration option fails in
    all sources.
    """


@dataclass
class ConfigLoadingIncomplete(Exception):
    """Throw when an attempt to load configurations fails to
    attend the defined constraints.
    """

    unlocated_keys: List[List[str]]
    invalid_keys: List[List[str]]
    expected_subtree_keys: List[List[str]]
    loaded_configs: dict


class UnrecognizedOS(Exception):
    """Throw when the operational system is not recognized."""


@dataclass
class InvalidOption(Exception):
    """Throw when a Option with validation finds a invalid value.
    Also works as a information dataclass to inform the problem
    in the configurations."""

    value: Any
    expected: Any


@dataclass
class NotSubtree(Exception):
    """Throw when trying to read a subtree structure such as a
    repeat, and finding a leaf node.
    """

    value: Any
