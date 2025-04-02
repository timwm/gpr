from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Subquery, OuterRef, F

from ..serializers import DepartmentSerializer, FacultySerializer
from ..models import Department, Faculty
from core.utils.io import IOMixin, paginate_response


class FacultyViewSet(IOMixin, viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=["get"], detail=True, url_path="departments", url_name="departments")
    def departments(self, request, *args, pk=None, **kwargs):
        try:
            departments = self.get_queryset().get(pk=pk).departments.all()
        except Faculty.DoesNotExist:
            raise ValidationError({'message': 'Faculty not found'})

        return paginate_response(self, departments, DepartmentSerializer)

    def get_queryset(self):
        return Faculty.objects.all() #prefetch_related('departments')


class DepartmentViewSet(IOMixin, viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Department.objects.all()
