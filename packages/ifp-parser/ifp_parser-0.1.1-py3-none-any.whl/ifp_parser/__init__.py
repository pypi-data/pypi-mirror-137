import configparser
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

_parser = configparser.ConfigParser()
_parser.read("pyproject.toml")
__version__ = _parser["tool.poetry"]["version"][1:-1]

from .parser import parse
