from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from authentication.serializers import LoginSerializer


class AccountViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
# class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        pass

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        pass
