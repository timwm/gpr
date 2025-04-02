"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from rest_framework import routers

if settings.DEBUG:
    router = routers.DefaultRouter(trailing_slash=False)
else:
    router = routers.SimpleRouter(trailing_slash=False)
router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(("api.urls", "api"), namespace="api")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('allauth.headless.urls')),
]
