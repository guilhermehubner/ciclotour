import sys

from ciclotour.api.paginator import (RoutePageNumberPagination,
                                     UserPageNumberPagination,
                                     RoutePicturePageNumberPagination,
                                     FeedPageNumberPagination, CommentsPageNumberPagination)
from ciclotour.api.serializers import (RouteSerializer,
                                       WayPointSerializer,
                                       UserProfileInfoSerializer,
                                       FieldKindSerializer,
                                       PointKindSerializer,
                                       PointSerializer,
                                       RoutePictureSerializer,
                                       CustomUserSerializer, RouteCommentSerializer, UserActivitySerializer,
                                       PointCommentSerializer)
from ciclotour.core.models import CustomUser, ConfirmationToken, UserActivity
from ciclotour.routes.models import Route, WayPoint, FieldKind, PointKind, Point, RoutePicture, RouteComment, \
    PointComment
from django.core import mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@permission_classes((IsAuthenticated, ))
class PointCommentListAPIView(ListAPIView):
    serializer_class = PointCommentSerializer
    queryset = PointComment.objects.all()
    pagination_class = CommentsPageNumberPagination

    def get_queryset(self):
        pointId = self.request.query_params.get("pointId", None)
        try:
            pointId = int(pointId)
        except:
            return PointComment.objects.none()

        return PointComment.objects.filter(point=pointId)


@permission_classes((IsAuthenticated, ))
class PointCommentCreateAPIView(CreateAPIView):
    serializer_class = PointCommentSerializer
    queryset = PointComment.objects.all()

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        UserActivity.objects.create(
            action=UserActivity.COMMENT,
            target=UserActivity.POINT,
            description=comment.description,
            user=self.request.user,
            point_comment=comment
        )


@permission_classes((IsAuthenticated, ))
class FeedListAPIView(ListAPIView):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()
    pagination_class = FeedPageNumberPagination

    def get_queryset(self):
        friends = self.request.user.get_friends_id()
        return UserActivity.objects.filter(user__in=friends)


@permission_classes((IsAuthenticated, ))
class RouteCommentListAPIView(ListAPIView):
    serializer_class = RouteCommentSerializer
    queryset = RouteComment.objects.all()
    pagination_class = CommentsPageNumberPagination

    def get_queryset(self):
        routeId = self.request.query_params.get("routeId", None)
        try:
            routeId = int(routeId)
        except:
            return RouteComment.objects.none()

        return RouteComment.objects.filter(route=routeId)


@permission_classes((IsAuthenticated, ))
class RouteCommentCreateAPIView(CreateAPIView):
    serializer_class = RouteCommentSerializer
    queryset = RouteComment.objects.all()

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        UserActivity.objects.create(
            action=UserActivity.COMMENT,
            target=UserActivity.ROUTE,
            description=comment.description,
            user=self.request.user,
            route_comment=comment
        )


@permission_classes((IsAuthenticated, ))
class PendingRoutesAPIView(ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    pagination_class = RoutePageNumberPagination

    def get_queryset(self):
        return self.request.user.pending_routes.all()


@permission_classes((IsAuthenticated, ))
class PerformedRoutesAPIView(ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    pagination_class = RoutePageNumberPagination

    def get_queryset(self):
        return self.request.user.performed_routes.all()


@permission_classes((IsAuthenticated, ))
class RoutesSearchAPIView(ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    pagination_class = RoutePageNumberPagination

    def get_queryset(self):
        from_latitude = self.request.query_params.get("from_lat", None)
        from_longitude = self.request.query_params.get("from_lng", None)

        to_latitude = self.request.query_params.get("to_lat", None)
        to_longitude = self.request.query_params.get("to_lng", None)

        try:
            from_latitude = float(from_latitude)
            from_longitude = float(from_longitude)
            to_latitude = float(to_latitude)
            to_longitude = float(to_longitude)
        except:
            return Route.objects.none()

        origin = WayPoint.objects.filter(latitude__gte=(from_latitude-0.05),
                                      latitude__lte=(from_latitude+0.05),
                                      longitude__gte=(from_longitude-0.05),
                                      longitude__lte=(from_longitude+0.05),
                                      kind=WayPoint.INITIAL).values_list('route_id', flat=True)

        ids = WayPoint.objects.filter(Q(kind=WayPoint.FINAL_GOOGLE) | Q(kind=WayPoint.FINAL_LINEAR),
                                      latitude__gte=(to_latitude-0.05),
                                      latitude__lte=(to_latitude+0.05),
                                      longitude__gte=(to_longitude-0.05),
                                      longitude__lte=(to_longitude+0.05),
                                      route_id__in=origin).values_list('route_id', flat=True)

        return Route.objects.filter(id__in=ids).filter(Q(shared_with=Route.PUBLIC) |
                                                       Q(shared_with=Route.PRIVATE, owner=self.request.user) |
                                                       Q(shared_with=Route.FRIENDS_ONLY,
                                                         owner__in=self.request.user.get_friends_id()) |
                                                       Q(shared_with=Route.FRIENDS_ONLY, owner=self.request.user.id))


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def mark_route_as_pending(request, routeId):
    get_object_or_404(Route, pk=routeId)

    if request.user.pending_routes.filter(pk=routeId).exists():
       request.user.pending_routes.remove(routeId)
       return Response({'marked': False}, status.HTTP_200_OK)

    if request.user.performed_routes.filter(pk=routeId).exists():
        request.user.performed_routes.remove(routeId)

    request.user.pending_routes.add(routeId)
    return Response({'marked': True}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def mark_route_as_performed(request, routeId):
    get_object_or_404(Route, pk=routeId)

    if request.user.performed_routes.filter(pk=routeId).exists():
       request.user.performed_routes.remove(routeId)
       return Response({'marked': False}, status.HTTP_200_OK)

    if request.user.pending_routes.filter(pk=routeId).exists():
        request.user.pending_routes.remove(routeId)

    request.user.performed_routes.add(routeId)
    return Response({'marked': True}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def unfriend(request, user_id):
    try:
        request.user.friends.remove(user_id)
        CustomUser.objects.get(pk=user_id).friends.remove(request.user.pk)
    except:
        ex = sys.exc_info()[0]
        return Response({'error': ex}, status.HTTP_400_BAD_REQUEST)

    return Response({'success': True}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def add_friend(request, user_id):
    try:
        request.user.friends.add(user_id)
    except:
        ex = sys.exc_info()[0]
        return Response({'error': ex}, status.HTTP_400_BAD_REQUEST)

    return Response({'success': True}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def refuse_request(request, user_id):
    try:
        CustomUser.objects.get(pk=user_id).friends.remove(request.user)
    except:
        ex = sys.exc_info()[0]
        return Response({'error': str(ex)}, status.HTTP_400_BAD_REQUEST)

    return Response({'success': True}, status.HTTP_200_OK)


@permission_classes((IsAuthenticated, ))
class PendingRequestsAPIView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user': self.request.user.id
        }

    def get_queryset(self):
        return self.request.user.get_pending_requests()


@permission_classes((IsAuthenticated, ))
class FriendsAPIView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = UserPageNumberPagination

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user': self.request.user.id
        }

    def get_queryset(self):
        return self.request.user.get_friends()


@permission_classes((IsAuthenticated, ))
class SearchUserAPIView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    pagination_class = UserPageNumberPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'last_name', 'email')

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user': self.request.user.id
        }

    def get_queryset(self):
        return super(SearchUserAPIView, self).get_queryset().filter(~Q(pk=self.request.user.id))


@api_view(['GET'])
def user_confirmation(request, token):
    confirmation_token = get_object_or_404(ConfirmationToken, token=token)
    user = confirmation_token.user

    if confirmation_token.is_active():
        user.is_active = True
        user.save()

        confirmation_token.delete()
        data = {'success': True}
    else:
        user.delete()
        data = {'success': False}

    return Response(data, status.HTTP_200_OK)


class CreateUserAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        validate_data = serializer.save()

        data = {
            'name': validate_data['name'],
            'last_name': validate_data['last_name'],
            'confirmation_link': 'http://' + self.request.META['HTTP_HOST'] +
                                 '/#/confirmation/' + validate_data['token'],
        }

        mail.send_mail('Confirmação de cadastro',
                       render_to_string('subscription_email.txt', data),
                       'eventex.testes@gmail.com',
                       [validate_data['email'], ]
                       )


@permission_classes((IsAuthenticated, ))
class UpdateUserAPIView(UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user


@permission_classes((IsAuthenticated, ))
class RoutePictureViewSet(ModelViewSet):
    serializer_class = RoutePictureSerializer
    queryset = RoutePicture.objects.all()
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('route',)
    pagination_class = RoutePicturePageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@permission_classes((IsAuthenticated, ))
class PointViewSet(ModelViewSet):
    serializer_class = PointSerializer
    queryset = Point.objects.all()
    lookup_field = 'id'


@permission_classes((IsAuthenticated, ))
class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    lookup_field = 'id'

    pagination_class = RoutePageNumberPagination

    def get_queryset(self):
        return Route.objects.filter(Q(shared_with=Route.PUBLIC) |
                                    Q(shared_with=Route.PRIVATE, owner=self.request.user) |
                                    Q(shared_with=Route.FRIENDS_ONLY,
                                      owner__in=self.request.user.get_friends_id()) |
                                    Q(shared_with=Route.FRIENDS_ONLY, owner=self.request.user.id))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def route_waypoints(request, route_id):
    waypoints = WayPoint.objects.filter(route__id=route_id)

    if waypoints.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WayPointSerializer(waypoints, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_logged(request):
    logged = False
    if request.user.is_authenticated():
        logged = True

    return Response({"logged": logged}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_profile_info(request):
    data = UserProfileInfoSerializer(request.user).data
    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def fields_list(request):
    data = FieldKindSerializer(FieldKind.objects.all(), many=True).data
    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def point_kind_list(request):
    data = PointKindSerializer(PointKind.objects.all(), many=True).data
    return Response(data, status.HTTP_200_OK)
