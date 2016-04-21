from ciclotour.routes.models import Route, WayPoint
from rest_framework.serializers import ModelSerializer


class WayPointSerializer(ModelSerializer):
    class Meta:
        model = WayPoint
        fields = ['kind', 'latitude', 'longitude']


class RouteSerializer(ModelSerializer):

    waypoint_set = WayPointSerializer(many=True)

    def create(self, validated_data):
        waypoints_data = validated_data.pop('waypoint_set')
        route = Route.objects.create(**validated_data)

        for waypoint_data in waypoints_data:
            WayPoint.objects.create(route=route, **waypoint_data)

        return route

    class Meta:
        model = Route
        fields = ['pk', 'title', 'origin', 'description', 'field', 'owner', 'waypoint_set', 'get_url']
        read_only_fields = ['pk', 'owner', 'get_url']
