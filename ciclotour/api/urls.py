from ciclotour.api.views import RouteViewSet
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'token-auth/$', obtain_auth_token)
]
