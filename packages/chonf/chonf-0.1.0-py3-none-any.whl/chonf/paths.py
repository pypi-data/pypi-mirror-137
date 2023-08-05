"""
      _                  __ 
  ___| |__   ___  _ __  / _|
 / __| '_ \ / _ \| '_ \| |_ 
| (__| | | | (_) | | | |  _|
 \___|_| |_|\___/|_| |_|_|  .core.paths

Provides default config paths for chonf.

Variables:

    default_path(author: str, name: str) -> List[pathlib.Path]:
        returns the paths to the user-wide and system-wide default
        configuration directories for the program running on the
        current system.

"""

from pathlib import Path
from typing import List
from os.path import expandvars
from functools import cache
from chonf.exceptions import UnrecognizedOS
from platform import system


@cache
def default_path(author: str, name: str) -> List[Path]:
    """Default config directory paths.

    Get the paths to the user-wide and system-wide default
    configuration directories for the program running on the
    current system.

    Args:
        author (str): Name of the author (company or person)
            of the program, used by Windows's default for
            program data files.
        name (str): Name of the program itself, that names
            the configuration directory under the system's
            default.

    """
    os = system()
    if os == "Linux":
        return [
            Path("~/.config/").expanduser() / name,
            Path("/etc/") / name,
        ]
    elif os == "Windows":
        return [
            Path(expandvars("%APPDATA%")) / author / name,
            Path(expandvars("%PROGRAMDATA%")) / author / name,
        ]
    elif os == "Darwin":  # macos
        return [
            Path("~/Library/Preferences/").expanduser() / name,
            Path("/Library/Preferences/") / name,
        ]
    else:
        raise UnrecognizedOS
