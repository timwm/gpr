from rest_framework import generics
from django.db.models import Value, Q, F
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity
)
from core.serializers import IssueSerializer
from .serializers import IssueQuerySerializer


class IssueSearch:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def build_query(self, extra):
        # TODO: For now we have ignored any validation errors
        if not isinstance(extra, dict):
            query = {}
            status = set(extra.getlist('status') + extra.getlist('status[]'))
            priority = set(extra.getlist('priority') + extra.getlist('priority[]'))
            escalation_level = set(extra.getlist('escalation_level') + extra.getlist('escalation_level[]'))

            if status:
                query['status'] = status
            if priority:
                query['priority'] = priority
            if escalation_level:
                query['escalation_level'] = escalation_level
        else:
            query = extra

        query_serializer = IssueQuerySerializer(data=extra)
        query_serializer.is_valid()

        validated_data = query_serializer.validated_data
        queries = {}
        for k, v in validated_data.items():
            query = getattr(self, 'build_%s_query' % k)(v)
            if query is not None:
                queries[k] = query

        return queries

    def search(self, query, extra, **kwargs):
        if query:
            ordering = kwargs['ordering']

            search_query = SearchQuery(query, search_type="websearch")
            vector = SearchVector("title", weight="A") + SearchVector("description", weight="B")
                    # + SearchVector("notes", weight="D")
            rank = SearchRank(vector, search_query,
                # weights=[0.1, 0.2, 0.4, 0.8],
                normalization=Value(2).bitor(Value(4))
            )
            similarity = TrigramSimilarity('title', query) + TrigramSimilarity('description', query)

            self.queryset = self.queryset.annotate(rank=rank, similarity=similarity) \
                .filter(Q(similarity__gt=0) | Q(rank__gt=0)) \
                .order_by('%ssimilarity' % ordering, '%srank' % ordering)
            # print([(i.rank,i.similarity) for i in self.queryset])

        if queries := self.build_query(extra):
            self.queryset = self.queryset.filter(*queries.values())

        return self.queryset if query or queries else None

    def build_owner_query(self, owner):
        kwargs = self._get_user_kwargs(owner)
        return self._get_query('owner', kwargs) if kwargs else None
    
    def build_assignee_query(self, assignee):
        kwargs = self._get_user_kwargs(assignee)
        return self._get_query('assignee', kwargs) if kwargs else None
    
    def build_categories_query(self, categories):
        kwargs = {}
        if categories:
            for c in categories:
                if isinstance(c, str) and (c := c.strip)() and not c:
                    continue
                try:
                    k, v = 'pk', int(c)
                except ValueError:
                    k, v = 'name', c
                kwargs.setdefault(k, []).append(v)

        return self._get_query('categories', kwargs) if kwargs else None

    def build_status_query(self, status):
        if status:
            return Q(status__in=status)
        return None

    def build_priority_query(self, priority):
        if priority:
            return Q(priority__in=priority)
        return None

    def build_escalation_level_query(self, escalation_level):
        if escalation_level:
            return Q(escalation_level__in=escalation_level)
        return None

    def build_before_query(self, before):
        return Q(created_at__lte=before)

    def build_after_query(self, after):
        return Q(created_at__gte=after)

    def _get_user_kwargs(self, users):
        kwargs = {}
        if users:
            for u in users:
                try:
                    k, v = 'pk', int(u)
                except ValueError:
                    if (u := u.strip()) and not u:
                        continue

                    if (i := u.rfind('@')) != -1 and u.rfind('.', i) != -1:
                        k, v = 'email', u
                    else:
                        k, v = 'username', u
                kwargs.setdefault(k, []).append(v)

        return kwargs

    def _get_query(self, name, kwargs):
        query = None
        for k, v in kwargs.items():
            # if k == 'email':
            #     for v in v:
            #         kw = {'%s__%s__icontains' % (name, k): v}
            #         if query is None:
            #             query = Q(**kw)
            #         else:
            #             query |= Q(**kw)
            #     continue
            
            kw = {'%s__%s__in' % (name, k): v}
            if query is None:
                query = Q(**kw)
            else:
                query |= Q(**kw)

        return query

