import re

from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity, TrigramDistance,
)
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Greatest


def prepare_search_term(term: str) -> str:
    """Sanitize the input term for a search using postgres to_tsquery.

    Cleans a search string to something acceptable for use with to_tsquery.
    Appends ':*' so that partial matches will also be returned.

    Args:
        term: the search term to be cleaned and prepared

    Returns:
        the prepared search string
    """

    query = re.sub(r'[!\'()|&]', ' ', term).strip()
    if query:
        query = re.sub(r'\s+', ' & ', query)
        query += ':*'
        # query = '*'+query

    return query


class ProductManager(models.Manager):

    def search(self, search_text):
        normalized_query = prepare_search_term(search_text)
        search_query = SearchQuery(
            normalized_query, config='english'
        )

        # search_query =search_text

        vector = SearchVector(
            StringAgg('name', delimiter=' '),
            weight='A',
            config='english',
        )
        queryset = self.get_queryset()
        qs = (

            queryset.annotate(
                rank=SearchRank(F('search_vector'), search_query),
                distance=TrigramDistance(StringAgg('name', delimiter=' '),  normalized_query)
                         + TrigramDistance('code', normalized_query)
                         + TrigramDistance(StringAgg('alternative_names', delimiter=' '), normalized_query
                ),

                 best_score=(F('rank')+F('distance'))/2
            )
            # .annotate(rank=search_rank )
            # .order_by('distance')

            .filter(Q(rank__gte=0.0) | Q(distance__gt=0.0)).order_by('best_score')[:20]
        )
        return qs