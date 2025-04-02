from django.urls import include, re_path
from .routers import router

versions = '|'.join( ("v1", ) )

urlpatterns = [
    #*router.urls,
    #re_path(f"api/(?P<version>({versions}))/", include(("api.routers", "api"), namespace="api")),
    re_path(f"(?P<version>({versions}))/", include((router.urls, "api"), namespace="api")),
]
