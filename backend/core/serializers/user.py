from ..models import User, Role
from rest_framework import serializers

from ..models import User, Role


class UserSerializer(serializers.ModelSerializer):
    #date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        exclude = ['password']
        read_only_field = ["id"]


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'
        read_only_field = ["id"]
