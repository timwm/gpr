from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
import environ, os


class ActiveSessionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    http_method_names = ["post"]
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        return Response({"success": True, }, status.HTTP_200_OK)
        
        #O11
        #login(request, request.user)
        #logout(request)

        d = request.session
        #env = environ.Env(DEBUG=(bool, False))
        data = {
            "success": True,

            #"e": os.environ,
            #"head": request.META["HTTP_X_CSRFTOKEN"],
            "t": str(type(d)),
            "as": str(request.authenticators),
            "d": d,
            "is_a": request.user.is_authenticated,
        }
        data.update({})
        return Response(data, status.HTTP_200_OK)
