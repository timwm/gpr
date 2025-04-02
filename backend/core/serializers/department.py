from ..models import Department, Faculty
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Department
        fields = '__all__'
        read_only_field = ["id"]


class FacultySerializer(serializers.ModelSerializer):

    #departments = DepartmentSerializer(many=True, read_only=True)
    departments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'
        read_only_field = ["id"]
