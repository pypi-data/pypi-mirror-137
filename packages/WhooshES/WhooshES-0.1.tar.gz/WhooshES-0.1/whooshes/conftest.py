import pytest

from whoosh import fields as f, qparser as qp


@pytest.fixture
def schema() -> f.Schema:
    """Default schema for testing containing many different field types."""
    return f.Schema(
        id=f.NUMERIC(bits=64, unique=True, stored=True, signed=False),
        key=f.ID(stored=True),
        datetime=f.DATETIME(sortable=True),
        text=f.TEXT(field_boost=0.5),
        int=f.NUMERIC(int),
        float=f.NUMERIC(float),
        bool=f.BOOLEAN(),
    )


@pytest.fixture
def qparser(schema: f.Schema) -> qp.QueryParser:
    """Convenience query parser for the default schema."""
    qparser = qp.QueryParser('key', schema)
    qparser.add_plugin(qp.RegexPlugin(expr='/(?P<text>[^/]*)/'))
    qparser.add_plugin(qp.FuzzyTermPlugin())
    return qparser
