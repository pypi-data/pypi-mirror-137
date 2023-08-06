__all__ = ['ESQueryTransformer']

from itertools import groupby
from typing import Dict, Any, Union, Tuple

from whoosh import query as q, fields as f
from whoosh.query import Query

from ..transformer import QueryTransformer

EsQ = Dict[str, Any]

SPAN_MULTITERM = q.FuzzyTerm, q.Prefix, q.Wildcard, q.Regex, q.RangeMixin,


class ESQueryTransformer(QueryTransformer[EsQ]):
    """Query transformer implementation for Elasticsearch."""

    def transform(self, query: Query) -> EsQ:
        return {'query': super().transform(query)}

    def handle_term(self, term: q.Term) -> EsQ:
        return self._build_term(term)

    def handle_variations(self, var: q.Variations) -> EsQ:
        return self._build_term(var, analyzer='english')

    def _build_term(self, _query: Union[q.Term, q.Variations], **kwargs) -> EsQ:
        name = _query.fieldname
        value = self._parse(name, _query.text)
        stype = self.schema[name]
        if isinstance(stype, f.TEXT):
            # Use match instead of term, recommended by term docs
            op, val_key = 'match', 'query'
        else:
            op, val_key = 'term', 'value'
        kwargs[val_key] = value
        return self._build_simple_op(_query, op, **kwargs)

    def handle_fuzzyterm(self, ft: q.FuzzyTerm) -> EsQ:
        return self._build_simple_op(
            ft, 'fuzzy',
            value=ft.text,
            fuzziness=ft.maxdist,
            prefix_length=ft.prefixlength,
            transpositions=True,
        )

    def handle_phrase(self, phrase: q.Phrase) -> EsQ:
        return self._build_simple_op(
            phrase, 'match_phrase',
            query=' '.join(phrase.words),
            slop=phrase.slop,
        )

    def handle_and(self, op: q.And) -> EsQ:
        return self._bool('must', op)

    def handle_or(self, op: q.Or) -> EsQ:
        query = self._bool('should', op)

        # Merge multiple term queries for the same field using terms
        subqs = query['bool']['should']

        def key_boost(s: EsQ) -> Tuple[str, float]:
            term = s['term']
            k = next(iter(term))
            return k, term[k].get('boost', 0.0)

        term_qs = sorted((s for s in subqs if 'term' in s), key=key_boost)
        for (key, boost), key_terms in groupby(term_qs, key=key_boost):
            key_terms = list(key_terms)
            if len(key_terms) > 1:
                for t in key_terms:
                    subqs.remove(t)
                values = [t['term'][key]['value'] for t in key_terms]
                terms = {'terms': {key: values}}
                if boost != 0:
                    terms['terms']['boost'] = boost
                subqs.append(terms)

        # Eliminate toplevel bool-should if only one sub-query
        if len(subqs) == 1:
            query = self._boost(op, subqs[0])

        return query

    def _bool(self, name: str, op: Union[q.And, q.Or]) -> EsQ:
        return {'bool': self._boost(op, {
            name: list(map(super().transform, op.subqueries)),
        })}

    def handle_disjunctionmax(self, dis: q.DisjunctionMax) -> EsQ:
        return {'dis_max': self._boost(
            dis,
            queries=list(map(super().transform, dis.subqueries)),
            tiebreak=dis.tiebreak,
        )}

    def handle_not(self, op: q.Not) -> EsQ:
        if isinstance(op.query, q.Or):  # Inline
            body = list(map(super().transform, op.query.subqueries))
        else:
            body = super().transform(op.query)
        return {'bool': self._boost(op, must_not=body)}

    def handle_prefix(self, pfx: q.Prefix) -> EsQ:
        return self._build_simple_op(pfx, 'prefix', value=pfx.text)

    def handle_wildcard(self, wc: q.Wildcard) -> EsQ:
        return self._build_simple_op(wc, 'wildcard', value=wc.text)

    def handle_regex(self, regex: q.Regex) -> EsQ:
        return self._build_simple_op(regex, 'regexp', value=regex.text)

    def _handle_range(self, rng: Union[q.TermRange,
                                       q.NumericRange,
                                       q.DateRange]) -> EsQ:
        name = rng.fieldname
        field = self.schema[name]
        start, end = rng.start, rng.end
        if isinstance(field, f.DATETIME):
            start, end = map(field.from_column_value, (start, end))
        params = {}
        if start is not None:
            params['gt' if rng.startexcl else 'gte'] = start
        if end is not None:
            params['lt' if rng.endexcl else 'lte'] = end
        return {'range': {name: self._boost(rng, params)}}

    handle_termrange = _handle_range
    handle_numericrange = _handle_range
    handle_daterange = _handle_range

    def handle_every(self, every: q.Every) -> EsQ:
        name = every.fieldname
        return {'exists': {'field': name}} if name else {'match_all': {}}

    def handle_nullquery(self, null: q.NullQuery) -> EsQ:
        return {}

    def handle_require(self, req: q.Require) -> EsQ:
        trans = super().transform
        return {'bool': self._boost(
            req,
            must=trans(req.a),
            filter=trans(req.b),
        )}

    def handle_andmaybe(self, am: q.AndMaybe) -> EsQ:
        trans = super().transform
        return {'bool': self._boost(
            am,
            must=trans(am.a),
            should=trans(am.b),
        )}

    def handle_andnot(self, an: q.AndNot) -> EsQ:
        return self.handle_and(q.And([an.a, q.Not(an.b)]))

    def handle_otherwise(self, ow: q.Otherwise) -> EsQ:
        # TODO: Maybe find a way to implement this?
        #       As far as I can tell, there is no way to say:
        #       "if query A yields no documents, return query B"
        raise NotImplementedError("Elasticsearch doesn't support otherwise")

    def handle_spanfirst(self, span: q.SpanFirst) -> EsQ:
        match = self._handle_spanclause(span.q)
        return {'span_first': self._boost(span, match=match, end=span.limit)}

    def handle_spannear(self, span: q.SpanNear) -> EsQ:
        return {'span_near': self._boost(
            span,
            clauses=list(map(self._handle_spanclause, (span.a, span.b))),
            slop=span.slop,
            in_order=span.ordered,
        )}

    def handle_spannear2(self, span: q.SpanNear2) -> EsQ:
        return {'span_near': self._boost(
            span,
            clauses=list(map(self._handle_spanclause, span.qs)),
            slop=span.slop,
            in_order=span.ordered,
        )}

    def handle_spannot(self, span: q.SpanNot) -> EsQ:
        return {'span_not': self._boost(
            span,
            include=self._handle_spanclause(span.a),
            exclude=self._handle_spanclause(span.b),
        )}

    def handle_spanor(self, span: q.SpanOr) -> EsQ:
        return {'span_or': self._boost(
            span,
            clauses=list(map(self._handle_spanclause, span.subqs)),
        )}

    def handle_spancontains(self, span: q.SpanContains) -> EsQ:
        return {'span_containing': self._boost(
            span,
            big=self._handle_spanclause(span.a),
            little=self._handle_spanclause(span.b),
        )}

    def handle_spanbefore(self, span: q.SpanBefore) -> EsQ:
        # I'm 95% sure this is close enough, TODO: Test
        return self.handle_spannear2(
            q.SpanNear2(
                [span.a, span.b],
                slop=999999,
                ordered=True,
            ),
        )

    def handle_spancondition(self, span: q.SpanCondition) -> EsQ:
        # TODO: Maybe find a way to implement this?
        raise NotImplementedError("Elasticsearch doesn't support SpanCondition")

    def _handle_spanclause(self, sq: q.Query) -> EsQ:
        if isinstance(sq, q.SpanQuery):
            body = super().transform(sq)
        elif isinstance(sq, q.Term):
            if not isinstance(sq.text, str):
                raise ValueError("Span terms can only be used with text")
            body = {'span_term': {sq.fieldname: sq.text}}
        elif isinstance(sq, SPAN_MULTITERM):
            body = {'span_multi': {'match': super().transform(sq)}}
        else:
            raise NotImplementedError(f"Unknown span query: {sq!r}")
        _remove_boost(body)
        return body

    def _parse(self, name: str, value: Any) -> Any:
        field = self.schema[name]
        if isinstance(value, bytes):
            return field.from_bytes(value)
        elif isinstance(field, f.DATETIME):
            return field.from_column_value(value)
        return value

    def _build_simple_op(self, _query: q.Query, _op: str, **body) -> EsQ:
        """
        Helper method to construct a basic operation in the form of:

        ``{<op>: {<field>: <body [+ boost]>}}``

        :param _query: Query to build operation for
        :param _op: Name of the operation, such as 'term' or 'match'
        :param body: Kwargs specifying fields for the body
        """
        return {_op: {_query.fieldname: self._boost(_query, body)}}

    def _boost(self, _query: q.Query, body: dict = None, **kwargs) -> dict:
        """
        Merge the body dictionary with the kwargs and apply the
        appropriate boost from either the given query or the field from
        the query.
        """
        if body is None:
            body = kwargs
        elif kwargs:
            body.update(kwargs)
        boost = getattr(_query, 'boost', 1.0)
        if boost == 1.0:
            try:
                boost = self.schema[_query.fieldname].format.field_boost
            except (AttributeError, KeyError):
                pass
        if boost != 1.0:
            body['boost'] = boost
        return body


def _remove_boost(body: dict):
    """
    Recursively remove the 'boost' keyword from the query. This is used
    for span queries as only the top level one can be boosted.
    """
    body.pop('boost', None)
    for k, v in body.items():
        if isinstance(v, dict):
            _remove_boost(v)
