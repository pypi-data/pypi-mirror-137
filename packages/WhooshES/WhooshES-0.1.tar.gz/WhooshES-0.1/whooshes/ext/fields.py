from typing import Union
from whoosh import fields
from whoosh.formats import Format
from whoosh.analysis.analyzers import LowercaseFilter

from .analyzers import SeparatedTokenizer


class SEPKEYWORD(fields.KEYWORD):  # noqa
    """
    Whoosh field type for fields containing seperated keyword-like data.
    This behaves like the built-in keyword, except that the separator
    can be specified with the ``sep`` parameter.
    """

    def __init__(self,
                 sep: str,
                 stored: bool = False,
                 lowercase: bool = False,
                 scorable: bool = False,
                 unique: bool = False,
                 field_boost: float = 1.0,
                 sortable: bool = False,
                 vector: Union[Format, bool] = None):
        analyzer = SeparatedTokenizer(sep)
        if lowercase:
            analyzer |= LowercaseFilter()
        super().__init__(
            stored=stored,
            scorable=scorable,
            unique=unique,
            field_boost=field_boost,
            sortable=sortable,
            vector=vector,
            analyzer=analyzer,
        )
