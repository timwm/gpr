# from api.authentication.viewsets import (
#     RegisterViewSet,
#     LoginViewSet,
#     ActiveSessionViewSet,
#     LogoutViewSet,
# )
import os
from django.urls import path
from django.conf import settings
from rest_framework import routers
# from api.user.viewsets import UserViewSet
# from .models.issue import get_attachment_storage # attachments_url
from .views import attachment as attachment_view

router = routers.SimpleRouter(trailing_slash=False)

# router.register(r"edit", UserViewSet, basename="user-edit")
#
# router.register(r"register", RegisterViewSet, basename="register")
#
# router.register(r"login", LoginViewSet, basename="login")
#
# router.register(r"checkSession", ActiveSessionViewSet, basename="check-session")
#
# router.register(r"logout", LogoutViewSet, basename="logout")

attachment_url = os.path.join(settings.MEDIA_URL.strip('/'), 'attachments/<uuid:file>')

urlpatterns = [
    *router.urls,
    path(attachment_url, attachment_view,),
]
