"""
Template Types Package
Imports template type implementations to register them
"""

from . import document
from . import code
from . import web_app
from . import data_science
from . import microservices

__all__ = ['document', 'code', 'web_app', 'data_science', 'microservices']
