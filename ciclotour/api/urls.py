from ciclotour.api.views import RouteViewSet, route_waypoints, user_logged, user_profile_info, fields_list, \
    point_kind_list, PointViewSet, RoutePictureViewSet, CreateUserAPIView, user_confirmation, UpdateUserAPIView, \
    SearchUserAPIView, add_friend, PendingRequestsAPIView, refuse_request, FriendsAPIView, unfriend, RoutesSearchAPIView
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
    url(r'^update-user/$', UpdateUserAPIView.as_view()),
    url(r'^token-auth/$', obtain_auth_token),
    url(r'^user-search/$', SearchUserAPIView.as_view()),
    url(r'^user-is-logged/$', user_logged),
    url(r'^user-profile-info/$', user_profile_info),
    url(r'^pending-requests/$', PendingRequestsAPIView.as_view()),
    url(r'^get-friends/$', FriendsAPIView.as_view()),
    url(r'^add-friend/(?P<user_id>[\d]+)/$', add_friend),
    url(r'^refuse-request/(?P<user_id>[\d]+)/$', refuse_request),
    url(r'^unfriend/(?P<user_id>[\d]+)/$', unfriend),
    url(r'^fields/$', fields_list),
    url(r'^pointkinds/$', point_kind_list),
    url(r'^route/waypoints/(?P<route_id>[\d]+)/$', route_waypoints),
    url(r'^confirmation/(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$',
        user_confirmation),
    url(r'^routes_search/', RoutesSearchAPIView.as_view())
]


