"""
ABSFUYU SPECIAL VERSION: LUCKGOD
--------------------------------
A small collection of code with a little bit luck ;)

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
    "stats", "pkg_data",
    # Other
    # "help", "pry", "version", "dev",
    # "everything",
]

# default function
from .help import *
from .pry import *
from .version import __version__
from .fun import happy_new_year

# default module
from . import calculation as cal
from . import data
from . import generator as gen
from . import lists
from . import strings
from . import util

# LUCK-BASED
from .code_red import luckgod as __luck
__luck()

if __name__ == "__main__":
    pass