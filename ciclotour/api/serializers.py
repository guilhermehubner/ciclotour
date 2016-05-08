from ciclotour.core.models import CustomUser, ConfirmationToken
from ciclotour.routes.models import Route, WayPoint, Polyline, FieldKind, PointKind, Point, RoutePicture
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)
    confirm_password = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'email', 'profile_picture', 'password', 'confirm_password']
        read_only_fields = ['pk']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def validate(self, data):
        if not data.get('password') and not data.get('confirm_password'):
            return data

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('As senhas não coincidem.')

        return data

    def create(self, validated_data):
        user = CustomUser(
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = str(ConfirmationToken.objects.create(user=user).token)

        validated_data['token'] = token

        return validated_data


class RoutePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePicture
        read_only_fields = ['pk', 'owner']


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
    pictures = RoutePictureSerializer(source='routepicture_set', many=True, read_only=True)

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
                  'waypoint_set', 'polyline_set', 'field_info', 'points', 'pictures']
        read_only_fields = ['pk', 'owner', 'field_info', 'points', 'pictures']
        extra_kwargs = {'field': {'write_only': True}}
