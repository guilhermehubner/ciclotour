from ciclotour.core.models import CustomUser
from ciclotour.routes.models import Route, WayPoint, Polyline, FieldKind, PointKind, Point
from rest_framework import serializers


class PointKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointKind
        read_only_fields = ['pk']


class PointSerializer(serializers.ModelSerializer):
    kind_info = PointKindSerializer(source='kind', read_only=True)

    class Meta:
        model = Point
        read_only_fields = ['pk']
        extra_kwargs = {'kind': {'write_only': True}}


class FieldKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldKind
        read_only_fields = ['pk']


class UserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'get_profile_pic']
        read_only_fields = ['pk']


class WayPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WayPoint
        fields = ['kind', 'latitude', 'longitude']
        read_only_fields = ['pk']


class PolylineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polyline
        fields = ['encoded_polyline']
        read_only_fields = ['pk']


class RouteSerializer(serializers.ModelSerializer):
    waypoint_set = WayPointSerializer(many=True)
    polyline_set = PolylineSerializer(many=True)
    points = PointSerializer(source='point_set', many=True, read_only=True)
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
                  'waypoint_set', 'polyline_set', 'field_info', 'points']
        read_only_fields = ['pk', 'owner', 'field_info', 'points']
        extra_kwargs = {'field': {'write_only': True}}
