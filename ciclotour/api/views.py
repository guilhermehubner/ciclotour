from ciclotour.api.paginator import RoutePagePageNumberPagination
from ciclotour.api.serializers import RouteSerializer, WayPointSerializer, UserProfileInfoSerializer, \
    FieldKindSerializer, PointKindSerializer, PointSerializer, RoutePictureSerializer, CustomUserSerializer
from ciclotour.core.models import CustomUser, ConfirmationToken
from ciclotour.routes.models import Route, WayPoint, FieldKind, PointKind, Point, RoutePicture
from django.core import mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


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

    pagination_class = RoutePagePageNumberPagination

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
