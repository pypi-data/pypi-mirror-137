from whoosh.analysis.filters import Filter


def SeparatedTokenizer(chars: str):  # noqa
    """
    Splits tokens by given characters.

    Note that the tokenizer calls unicode.strip() on each match of the
    regular expression.

    >>> cst = SeparatedTokenizer(';')
    >>> [token.text for token in cst("hi there; what's ; up")]
    ['hi there', "what's", 'up']
    """
    from whoosh.analysis.tokenizers import RegexTokenizer
    from whoosh.analysis.filters import StripFilter

    return RegexTokenizer(f"[^{chars}]+") | StripFilter()


class UppercaseFilter(Filter):
    """
    Uses str.upper() to lowercase token text.

    >>> from whoosh.analysis.tokenizers import RegexTokenizer
    >>> rext = RegexTokenizer()
    >>> stream = rext("This is a TEST")
    >>> [token.text for token in UppercaseFilter()(stream)]
    ['THIS', 'IS', 'A', 'TEST']
    """

    def __call__(self, tokens):
        for t in tokens:
            t.text = t.text.upper()
            yield t
