from ciclotour.core.models import CustomUser, ConfirmationToken, UserActivity
from ciclotour.routes.models import Route, WayPoint, Polyline, FieldKind, PointKind, Point, RoutePicture, RouteComment, \
    PointComment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PointCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointComment
        fields = ['user', 'description', 'point', 'published', 'user_name', 'user_photo']
        read_only_fields = ['user', 'published', 'user_name', 'user_photo']


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['action_name', 'target_name', 'description', 'date',
                  'user_name', 'user_photo', 'target_link', 'target_object_name']
        read_only_fields = ['action_name', 'target_name', 'description', 'date',
                            'user_name', 'user_photo', 'target_link', 'target_object_name']


class RouteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteComment
        fields = ['user', 'description', 'route', 'published', 'user_name', 'user_photo']
        read_only_fields = ['user', 'published', 'user_name', 'user_photo']


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)
    friendship_status = serializers.SerializerMethodField('_friendship_status')

    class Meta:
        model = CustomUser
        fields = ['pk', 'name', 'last_name', 'email', 'profile_picture', 'password',
                  'confirm_password', 'get_profile_pic', 'friendship_status', 'get_friends_count',
                  'pending_routes_count', 'performed_routes_count']
        read_only_fields = ['pk', 'get_profile_pic', 'friendship_status', 'get_friends_count',
                            'pending_routes_count', 'performed_routes_count']
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
        extra_kwargs = {'profile_picture': {'write_only': True}}

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

    def _friendship_status(self, obj):
        return obj.get_friendship_status(self.context['user'])


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
        fields = ['name', 'last_name', 'get_profile_pic', 'get_friends_count',
                  'get_pending_requests_count', 'pending_routes_count', 'performed_routes_count']
        read_only_fields = ['pk'] + fields


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

        wp = None
        for waypoint_data in waypoints_data:
            wp = WayPoint.objects.create(route=route, **waypoint_data)

        if wp.kind == WayPoint.GOOGLE:
            wp.kind = WayPoint.FINAL_GOOGLE
        else:
            wp.kind = WayPoint.FINAL_LINEAR

        wp.save()

        for polyline_data in polylines_data:
            Polyline.objects.create(route=route, **polyline_data)

        return route

    def validate(self, data):
        if len(data.get('waypoint_set')) == 0 or len(data.get('polyline_set')) == 0:
            raise serializers.ValidationError('Deve-se traçar uma rota!')

        return data

    class Meta:
        model = Route
        fields = ['pk', 'title', 'origin', 'description', 'field', 'owner',
                  'waypoint_set', 'polyline_set', 'field_info', 'points', 'pictures', 'get_picture',
                  'shared_with']
        read_only_fields = ['pk', 'owner', 'field_info', 'points', 'pictures', 'get_picture']
        extra_kwargs = {'field': {'write_only': True}}
