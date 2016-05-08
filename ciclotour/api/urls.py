from ciclotour.api.views import RouteViewSet, route_waypoints, user_logged, user_profile_info, fields_list, \
    point_kind_list, PointViewSet, RoutePictureViewSet, CreateUserAPIView, user_confirmation
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'route/points', PointViewSet)
router.register(r'route/pictures', RoutePictureViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create-user/$', CreateUserAPIView.as_view()),
    url(r'^token-auth/$', obtain_auth_token),
    url(r'^user-is-logged/$', user_logged),
    url(r'^user-profile-info/$', user_profile_info),
    url(r'^fields/$', fields_list),
    url(r'^pointkinds/$', point_kind_list),
    url(r'^route/waypoints/(?P<route_id>[\d]+)/$', route_waypoints),
    url(r'^confirmation/(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$',
        user_confirmation)
]


