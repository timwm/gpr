from django.db.models import Subquery, OuterRef, F
from django.http import QueryDict
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.utils.io import IOMixin, paginate_response
from core.models import Issue
from core.serializers import IssueSerializer
from .search import IssueSearch
from .serializers import IssueQuerySerializer


class SearchViewSet(IOMixin, viewsets.GenericViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)

    # @action(methods=["GET"], detail=True, url_path="departments", url_name="departments")
    def list(self, request, *args, **kwargs):
        # except Faculty.DoesNotExist:
        #     raise ValidationError({'message': 'Faculty not found'})

        # return Response(request.query_params)
        return self.search(request.query_params)

        return paginate_response(self, result, IssueSerializer)

    def create(self, request, *args, **kwargs):
        #return self.list(request, *args, **kwargs)
        return self.search(request.data)
        return Response({'hello':'World', 'data':request.data})

    def search(self, query_obj):
        if isinstance(query_obj, QueryDict):
            extra = QueryDict(mutable=True)
            extra.update(query_obj)
            q = extra.pop('q', [None])[-1] or None
            ordering = extra.pop('sort', ['DESC'])[-1]
        else:
            extra = query_obj.copy()
            q = extra.pop('q', None) or None
            ordering = extra.pop('sort', 'DESC')

        if q and (q := q.strip()) and len(q) > 4096:
            return Response(
                {'detail': 'Query payload too large'},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        kwargs = {
            'ordering': '-' if ordering.lower() == 'desc' else ''
        }

        result = IssueSearch(self.get_queryset()).search(q, extra, **kwargs)
        # print({'query':str(result.query)})

        return Response(IssueSerializer(result, many=True).data)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Issue.objects.all()
        return Issue.objects.filter(owner=user)
