from ciclotour.core.models import CustomUser
from ciclotour.routes.models import Route, WayPoint, Polyline, FieldKind
from rest_framework import serializers


class FieldKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldKind


class UserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'get_profile_pic']


class WayPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WayPoint
        fields = ['kind', 'latitude', 'longitude']


class PolylineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polyline
        fields = ['encoded_polyline']


class RouteSerializer(serializers.ModelSerializer):
    waypoint_set = WayPointSerializer(many=True)
    polyline_set = PolylineSerializer(many=True)
    field_info = FieldKindSerializer(source='field', read_only=True)

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
                  'waypoint_set', 'polyline_set', 'field_info']
        read_only_fields = ['pk', 'owner', 'field_info']
