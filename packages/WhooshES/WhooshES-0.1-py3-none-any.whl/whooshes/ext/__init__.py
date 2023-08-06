"""
Whoosh Extensions
=================

This package provides various extensions to the Whoosh library, such as
new fields and analyzers, that may be convenient when interacting with
Whoosh.

.. note::
    While these aren't for providing compatibility with Elasticsearch
    and beyond, I didn't feel that they warranted their own package and
    repo, so here they are.
"""

__all__ = [
    'SeparatedTokenizer',
    'UppercaseFilter',
    'SEPKEYWORD',
]

from .analyzers import SeparatedTokenizer, UppercaseFilter
from .fields import SEPKEYWORD
