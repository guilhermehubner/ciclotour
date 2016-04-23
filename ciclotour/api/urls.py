from ciclotour.api.views import RouteViewSet, route_waypoints
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token-auth/$', obtain_auth_token),
    url(r'^route/waypoints/(?P<route_id>[\d]+)/$', route_waypoints),
]
