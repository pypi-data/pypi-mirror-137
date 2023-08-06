import abc
from functools import lru_cache

from typing import Type, Generic, Callable, TypeVar

from whoosh import query as q, fields as f

T = TypeVar('T')


class QueryTransformer(abc.ABC, Generic[T]):
    """
    Abstract base class declaring the interface for Whoosh Query
    transformers which take a :class:`~whoosh.query.qcore.Query`
    instance and convert it to appropriate object for querying the
    target database. For example, in Elasticsearch, the output query
    is a nested dictionary.

    To implement a transformer for a new target, developers should
    create a subclass and implement all of the abstract ``handle_*``
    methods. As not all databases have the same features, it is expected
    that handling one or more of the query types is not possible.
    In these cases, the method should simply raise
    :class:`NotImplementedError` with an explanation.

    See :class:`~whooshes.elasticsearch.transformer.ESQueryTransformer`
    for the reference implementation.
    """

    def __init__(self, schema: f.Schema):
        self.schema = schema
        setattr(self, 'get_method', lru_cache(maxsize=None)(self.get_method))

    def transform(self, query: q.Query) -> T:
        """
        Transform a given query object as necessary for the target
        backend.
        """
        return self.get_method(query.__class__)(query)

    def get_method(self, tquery: Type[q.Query]) -> Callable[[q.Query], T]:
        """
        Get the particular method which should handle transforming the
        given query type. This method has a per-instance LRU cache
        applied during initialization to minimize overhead.
        """
        name = tquery.__name__.lower().strip('_')
        try:
            return getattr(self, f'handle_{name}')
        except AttributeError:
            raise NotImplementedError(f"Unknown query type: {tquery}")

    # Queries handler order should match the docs for ease of reading

    # Query Classes
    # https://whoosh.readthedocs.io/en/latest/api/query.html#query-classes

    @abc.abstractmethod
    def handle_term(self, term: q.Term) -> T:
        pass

    @abc.abstractmethod
    def handle_variations(self, var: q.Variations) -> T:
        pass

    @abc.abstractmethod
    def handle_fuzzyterm(self, ft: q.FuzzyTerm) -> T:
        pass

    @abc.abstractmethod
    def handle_phrase(self, phrase: q.Phrase) -> T:
        pass

    @abc.abstractmethod
    def handle_and(self, op: q.And) -> T:
        pass

    @abc.abstractmethod
    def handle_or(self, op: q.Or) -> T:
        pass

    @abc.abstractmethod
    def handle_disjunctionmax(self, dis: q.DisjunctionMax) -> T:
        pass

    @abc.abstractmethod
    def handle_not(self, op: q.Not) -> T:
        pass

    @abc.abstractmethod
    def handle_prefix(self, pfx: q.Prefix) -> T:
        pass

    @abc.abstractmethod
    def handle_wildcard(self, wc: q.Wildcard) -> T:
        pass

    @abc.abstractmethod
    def handle_regex(self, regex: q.Regex) -> T:
        pass

    @abc.abstractmethod
    def handle_termrange(self, rng: q.TermRange) -> T:
        pass

    @abc.abstractmethod
    def handle_numericrange(self, rng: q.NumericRange) -> T:
        pass

    @abc.abstractmethod
    def handle_daterange(self, rng: q.DateRange) -> T:
        pass

    @abc.abstractmethod
    def handle_every(self, every: q.Every) -> T:
        pass

    @abc.abstractmethod
    def handle_nullquery(self, null: q.NullQuery) -> T:
        pass

    # Binary Queries
    # https://whoosh.readthedocs.io/en/latest/api/query.html#binary-queries

    @abc.abstractmethod
    def handle_require(self, req: q.Require) -> T:
        pass

    @abc.abstractmethod
    def handle_andmaybe(self, am: q.AndMaybe) -> T:
        pass

    @abc.abstractmethod
    def handle_andnot(self, an: q.AndNot) -> T:
        pass

    @abc.abstractmethod
    def handle_otherwise(self, ow: q.Otherwise) -> T:
        pass

    # Span Queries
    # https://whoosh.readthedocs.io/en/latest/api/query.html#span-queries

    @abc.abstractmethod
    def handle_spanfirst(self, span: q.SpanFirst) -> T:
        pass

    @abc.abstractmethod
    def handle_spannear(self, span: q.SpanNear) -> T:
        pass

    @abc.abstractmethod
    def handle_spannear2(self, span: q.SpanNear2) -> T:
        pass

    @abc.abstractmethod
    def handle_spannot(self, span: q.SpanNot) -> T:
        pass

    @abc.abstractmethod
    def handle_spanor(self, span: q.SpanOr) -> T:
        pass

    @abc.abstractmethod
    def handle_spancontains(self, span: q.SpanContains) -> T:
        pass

    @abc.abstractmethod
    def handle_spanbefore(self, span: q.SpanBefore) -> T:
        pass

    @abc.abstractmethod
    def handle_spancondition(self, span: q.SpanCondition) -> T:
        pass

    # Special Queries
    # https://whoosh.readthedocs.io/en/latest/api/query.html#special-queries

    # TODO: Nested parents, etc
