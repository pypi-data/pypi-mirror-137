"""
Toontown Rewritten API Wrapper
==============================

A basic wrapper for the Toontown Rewritten API

:copyright: (c) 2022-present jaczerob
:license: MIT, see LICENSE for more details.
"""

__title__ = 'toontown'
__author__ = 'jaczerob'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present jaczerob'
__version__ = '1.0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging

from .client import *
from .exceptions import *
from .httpclient import *

logging.getLogger(__name__).addHandler(logging.NullHandler())
