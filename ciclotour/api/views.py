from ciclotour.api.serializers import RouteSerializer, WayPointSerializer, UserProfileInfoSerializer
from ciclotour.routes.models import Route, WayPoint
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@permission_classes((IsAuthenticated, ))
class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['owner'] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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