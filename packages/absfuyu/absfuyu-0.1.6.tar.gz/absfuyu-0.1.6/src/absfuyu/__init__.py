"""
ABSFUYU
-------
A small collection of code

HOMEPAGE
--------
`https://pypi.org/project/absfuyu/`

USAGE
-----
import absfuyu

absfuyu.help()
"""


__title__ = "absfuyu"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__all__ = [
    # default
    "calculation", "data", "generator",
    "strings", "util", "lists",
    # extra
    "fibonacci", "obfuscator", "sort", "fun",
    "stats",
    # Other
    #"help", "pry", "version",
    # "everything"
]

# default function
from .help import *
from .pry import *
from .version import __version__
from .fun import happy_new_year

# default module
from . import calculation
from . import data
from . import generator
from . import lists
from . import strings
from . import util



if __name__ == "__main__":
    pass