from ciclotour.api.views import RouteViewSet, route_waypoints, user_logged, user_profile_info
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token-auth/$', obtain_auth_token),
    url(r'^user-is-logged/$', user_logged),
    url(r'^user-profile-info/$', user_profile_info),
    url(r'^route/waypoints/(?P<route_id>[\d]+)/$', route_waypoints),
]
