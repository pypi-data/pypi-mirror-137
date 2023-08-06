from datetime import datetime
from typing import Dict, Callable, Any, Union

import pytest

from whoosh import query as q, fields as f, qparser as qp

from whooshes.elasticsearch.transformer import ESQueryTransformer

ToES = Callable[[Union[str, q.Query]], Dict[str, Any]]


@pytest.fixture
def qtrans(schema: f.Schema) -> ESQueryTransformer:
    return ESQueryTransformer(schema)


@pytest.fixture
def to_es(qtrans: ESQueryTransformer,
          schema: f.Schema,
          qparser: qp.QueryParser) -> ToES:
    def _to_es(query: Union[str, q.Query]) -> Dict[str, Any]:
        if isinstance(query, str):
            query = qparser.parse(query)
        return qtrans.transform(query)['query']

    return _to_es


def test_term(to_es: ToES):
    assert to_es('id:10') == {'term': {'id': {'value': 10}}}
    assert to_es('key:a') == {'term': {'key': {'value': 'a'}}}
    assert to_es('text:abc') == {'match': {
        'text': {'query': 'abc', 'boost': 0.5},
    }}
    assert to_es('int:10') == {'term': {'int': {'value': 10}}}
    assert to_es('float:1.4') == {'term': {'float': {'value': 1.4}}}
    assert to_es('bool:1') == {'term': {'bool': {'value': True}}}
    assert to_es('bool:True') == {'term': {'bool': {'value': True}}}


def test_variations(to_es: ToES):
    assert to_es(q.Variations('text', 'run')) == {'match': {'text': {
        'query': 'run',
        'analyzer': 'english',
        'boost': 0.5,
    }}}


def test_fuzzyterm(to_es: ToES):
    assert to_es("text:bac~3/2") == {'fuzzy': {'text': {
        'value': 'bac',
        "fuzziness": 3,
        "prefix_length": 2,
        "transpositions": True,
        'boost': 0.5,
    }}}


def test_phrase(to_es: ToES):
    assert to_es('text:"these words"') == {'match_phrase': {'text': {
        'query': 'these words',
        "slop": 1,
        'boost': 0.5,
    }}}
    assert to_es('text:"these words"~2') == {'match_phrase': {'text': {
        'query': 'these words',
        "slop": 2,
        'boost': 0.5,
    }}}


def test_and(to_es: ToES):
    assert to_es("key:a int:1") == {'bool': {'must': [
        {'term': {'key': {'value': 'a'}}},
        {'term': {'int': {'value': 1}}},
    ]}}
    assert to_es("text:abc AND int:1") == {'bool': {'must': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'term': {'int': {'value': 1}}},
    ]}}
    assert to_es("text:abc int:[1 to 2]") == {'bool': {'must': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'range': {'int': {'gte': 1, 'lte': 2}}},
    ]}}


def test_or(to_es: ToES):
    assert to_es("key:a OR int:1") == {'bool': {'should': [
        {'term': {'key': {'value': 'a'}}},
        {'term': {'int': {'value': 1}}},
    ]}}
    assert to_es("text:abc OR int:1") == {'bool': {'should': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'term': {'int': {'value': 1}}},
    ]}}
    assert to_es("text:abc OR int:[1 to 2]") == {'bool': {'should': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'range': {'int': {'gte': 1, 'lte': 2}}},
    ]}}


def test_or_optimize(to_es: ToES):
    assert to_es("key:a OR key:b") == {'terms': {'key': ['a', 'b']}}
    assert to_es("key:a OR key:b^2 OR key:c") == {'bool': {'should': [
        {'term': {'key': {'value': 'b', 'boost': 2.0}}},
        {'terms': {'key': ['a', 'c']}},
    ]}}
    assert to_es("key:a OR int:1 OR key:b") == {'bool': {'should': [
        {'term': {'int': {'value': 1}}},
        {'terms': {'key': ['a', 'b']}},
    ]}}
    assert to_es("(key:a OR key:b)^2") == {
        'terms': {'key': ['a', 'b']},
        'boost': 2.0,
    }


def test_disjunctionmax(to_es: ToES, qparser: qp.QueryParser):
    subqs = list(map(qparser.parse, ['text:abc', 'int:1']))
    assert to_es(q.DisjunctionMax(subqs)) == {'dis_max': {
        'queries': [
            {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
            {'term': {'int': {'value': 1}}},
        ],
        'tiebreak': 0.0,
    }}


def test_not(to_es: ToES):
    assert to_es("NOT int:1") == {'bool': {'must_not': {
        'term': {'int': {'value': 1}},
    }}}
    assert to_es("NOT (text:abc AND int:1)") == {'bool': {'must_not': {
        'bool': {'must': [
            {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
            {'term': {'int': {'value': 1}}},
        ]},
    }}}
    assert to_es("NOT (text:abc OR int:1)") == {'bool': {'must_not': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'term': {'int': {'value': 1}}},
    ]}}


def test_prefix(to_es: ToES):
    assert to_es("text:ab*") == {'prefix': {
        'text': {'value': 'ab', 'boost': 0.5},
    }}


def test_wildcard(to_es: ToES):
    assert to_es("text:a*c") == {'wildcard': {
        'text': {'value': 'a*c', 'boost': 0.5},
    }}


def test_regex(to_es: ToES):
    assert to_es("text:/abc/") == {'regexp': {
        'text': {'value': 'abc', 'boost': 0.5},
    }}


def test_inclusive_range(to_es: ToES):
    assert to_es("key:[a to c]") \
           == {'range': {'key': {'gte': 'a', 'lte': 'c'}}}
    assert to_es("text:[a to c]") \
           == {'range': {'text': {'gte': 'a', 'lte': 'c', 'boost': 0.5}}}
    assert to_es("int:[10 to 20]") \
           == {'range': {'int': {'gte': 10, 'lte': 20}}}
    assert to_es("float:[.2 to 1.2]") \
           == {'range': {'float': {'gte': .2, 'lte': 1.2}}}


def test_exclusive_range(to_es: ToES):
    assert to_es("key:{a to c}") \
           == {'range': {'key': {'gt': 'a', 'lt': 'c'}}}
    assert to_es("text:{a to c}") \
           == {'range': {'text': {'gt': 'a', 'lt': 'c', 'boost': 0.5}}}
    assert to_es("int:{10 to 20}") \
           == {'range': {'int': {'gt': 10, 'lt': 20}}}
    assert to_es("float:{.2 to 1.2}") \
           == {'range': {'float': {'gt': .2, 'lt': 1.2}}}


def test_exclusive_lower_range(to_es: ToES):
    assert to_es("key:{a to c]") \
           == {'range': {'key': {'gt': 'a', 'lte': 'c'}}}
    assert to_es("text:{a to c]") \
           == {'range': {'text': {'gt': 'a', 'lte': 'c', 'boost': 0.5}}}
    assert to_es("int:{10 to 20]") \
           == {'range': {'int': {'gt': 10, 'lte': 20}}}
    assert to_es("float:{.2 to 1.2]") \
           == {'range': {'float': {'gt': .2, 'lte': 1.2}}}


def test_exclusive_upper_range(to_es: ToES):
    assert to_es("key:[a to c}") \
           == {'range': {'key': {'gte': 'a', 'lt': 'c'}}}
    assert to_es("text:[a to c}") \
           == {'range': {'text': {'gte': 'a', 'lt': 'c', 'boost': 0.5}}}
    assert to_es("int:[10 to 20}") \
           == {'range': {'int': {'gte': 10, 'lt': 20}}}
    assert to_es("float:[.2 to 1.2}") \
           == {'range': {'float': {'gte': .2, 'lt': 1.2}}}


def test_unbounded_upper_range(to_es: ToES):
    assert to_es("key:[a to]") == {'range': {'key': {'gte': 'a'}}}
    assert to_es("text:[a to]") == {'range': {
        'text': {'gte': 'a', 'boost': 0.5},
    }}
    assert to_es("int:[10 to]") == {'range': {'int': {'gte': 10}}}
    assert to_es("float:[.2 to]") == {'range': {'float': {'gte': .2}}}


def test_unbounded_lower_range(to_es: ToES):
    assert to_es("key:[to c}") == {'range': {'key': {'lt': 'c'}}}
    assert to_es("text:[to c}") == {'range': {
        'text': {'lt': 'c', 'boost': 0.5},
    }}
    assert to_es("int:[to 20}") == {'range': {'int': {'lt': 20}}}
    assert to_es("float:[to 1.2}") == {'range': {'float': {'lt': 1.2}}}


def test_date_range(to_es: ToES):
    assert to_es("datetime:2019-10-10") == {'range': {'datetime': {
        'gte': datetime(2019, 10, 10),
        'lte': datetime(2019, 10, 10, 23, 59, 59, 999999),
    }}}
    assert to_es("datetime:20191010") == {'range': {'datetime': {
        'gte': datetime(2019, 10, 10),
        'lte': datetime(2019, 10, 10, 23, 59, 59, 999999),
    }}}
    assert to_es("datetime:[20191010 to 20191011]") == {'range': {'datetime': {
        'gte': datetime(2019, 10, 10),
        'lte': datetime(2019, 10, 11, 23, 59, 59, 999999),
    }}}


def test_every(to_es: ToES):
    assert to_es("key:*") == {'exists': {'field': 'key'}}
    assert to_es("*:*") == {'match_all': {}}


def test_nullquery(to_es: ToES):
    assert to_es("") == {}


def test_require(to_es: ToES):
    assert to_es('text:abc REQUIRE int:1') == {'bool': {
        'must': {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        'filter': {'term': {'int': {'value': 1}}},
    }}


def test_andmaybe(to_es: ToES):
    assert to_es('text:abc ANDMAYBE int:1') == {'bool': {
        'must': {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        'should': {'term': {'int': {'value': 1}}},
    }}


def test_andnot(to_es: ToES):
    assert to_es('text:abc ANDNOT int:1') == {'bool': {'must': [
        {'match': {'text': {'query': 'abc', 'boost': 0.5}}},
        {'bool': {'must_not': {'term': {'int': {'value': 1}}}}},
    ]}}


def test_otherwise(to_es: ToES, qparser: qp.QueryParser):
    with pytest.raises(NotImplementedError):
        to_es(q.Otherwise(*map(qparser.parse, ['text:abc', 'int:1'])))


def test_spanfirst(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(q.SpanFirst(qparser.parse('text:abc'), 3)) == {
        'span_first': {
            'match': {'span_term': {'text': 'abc'}},
            'end': 3,
        }
    }


def test_spanmulti(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(q.SpanFirst(qparser.parse('text:a*'), 3)) == {
        'span_first': {
            'match': {
                'span_multi': {'match': {'prefix': {'text': {'value': 'a'}}}},
            },
            'end': 3,
        }
    }


def test_spannear(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(
        q.SpanNear(
            *map(qparser.parse, ['text:abc', 'key:a']),
            slop=3,
            ordered=False,
        )
    ) == {'span_near': {
        'clauses': [
            {'span_term': {'text': 'abc'}},
            {'span_term': {'key': 'a'}},
        ],
        'slop': 3,
        'in_order': False,
    }}


def test_spannear2(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(
        q.SpanNear2(
            list(map(qparser.parse, ['text:abc', 'key:a', 'text:bac'])),
            slop=3,
            ordered=False,
        )
    ) == {'span_near': {
        'clauses': [
            {'span_term': {'text': 'abc'}},
            {'span_term': {'key': 'a'}},
            {'span_term': {'text': 'bac'}},
        ],
        'slop': 3,
        'in_order': False,
    }}


def test_spannot(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(q.SpanNot(*map(qparser.parse, ['text:abc', 'key:a']))) == {
        'span_not': {
            'include': {'span_term': {'text': 'abc'}},
            'exclude': {'span_term': {'key': 'a'}},
        }
    }


def test_spanor(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(
        q.SpanOr(list(map(qparser.parse, ['text:abc', 'key:a', 'text:bac'])))
    ) == {'span_or': {
        'clauses': [
            {'span_term': {'text': 'abc'}},
            {'span_term': {'key': 'a'}},
            {'span_term': {'text': 'bac'}},
        ],
    }}


def test_spanbefore(to_es: ToES, qparser: qp.QueryParser):
    assert to_es(q.SpanBefore(*map(qparser.parse, ['text:abc', 'key:a']))) == {
        'span_near': {
            'clauses': [
                {'span_term': {'text': 'abc'}},
                {'span_term': {'key': 'a'}},
            ],
            'slop': 999999,
            'in_order': True,
        }
    }


def test_spancondition(to_es: ToES, qparser: qp.QueryParser):
    with pytest.raises(NotImplementedError):
        to_es(q.SpanCondition(*map(qparser.parse, ['text:abc', 'key:a'])))


def test_query_boost(to_es: ToES):
    assert to_es("key:a^5.0 int:1^2.0") == {'bool': {'must': [
        {'term': {'key': {'value': 'a', 'boost': 5.0}}},
        {'term': {'int': {'value': 1, 'boost': 2.0}}},
    ]}}


def test_nested_or(to_es: ToES):
    assert to_es(q.Or([
        q.Term('key', 'a'),
        q.Or([q.Term('int', 1), q.Term('key', 'b')])
    ])) == {'bool': {'should': [
        {'term': {'key': {'value': 'a'}}},
        {'bool': {
            'should': [
                {'term': {'int': {'value': 1}}},
                {'term': {'key': {'value': 'b'}}},
            ]
        }},
    ]}}
    assert to_es(q.Or([
        q.Term('key', 'a'),
        q.Or([q.Term('int', 1), q.Term('int', 2)])
    ])) == {'bool': {'should': [
        {'term': {'key': {'value': 'a'}}},
        {'terms': {'int': [1, 2]}},
    ]}}

