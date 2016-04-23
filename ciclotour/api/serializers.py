from ciclotour.routes.models import Route, WayPoint, Polyline
from rest_framework.serializers import ModelSerializer


class WayPointSerializer(ModelSerializer):
    class Meta:
        model = WayPoint
        fields = ['kind', 'latitude', 'longitude']


class PolylineSerializer(ModelSerializer):
    class Meta:
        model = Polyline
        fields = ['encoded_polyline']


class RouteSerializer(ModelSerializer):

    waypoint_set = WayPointSerializer(many=True)
    polyline_set = PolylineSerializer(many=True)

    def create(self, validated_data):
        waypoints_data = validated_data.pop('waypoint_set')
        polylines_data = validated_data.pop('polyline_set')
        route = Route.objects.create(**validated_data)

        for waypoint_data in waypoints_data:
            WayPoint.objects.create(route=route, **waypoint_data)

        for polyline_data in polylines_data:
            Polyline.objects.create(route=route, **polyline_data)

        return route

    class Meta:
        model = Route
        fields = ['pk', 'title', 'origin', 'description', 'field', 'owner',
                  'waypoint_set', 'get_url', 'polyline_set']
        read_only_fields = ['pk', 'owner', 'get_url']
