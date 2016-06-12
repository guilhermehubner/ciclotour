import uuid
from datetime import timedelta, datetime

from ciclotour.core.managers import CustomUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


def _user_profile_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]
    return 'users_profile/user_{}/profile.{}'.format(instance.email, file_extension)


def _now_plus_7():
    date = datetime.now() + timedelta(days=7)
    return date.replace(hour=23, minute=59, second=59, microsecond=0)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    FRIENDS = 'F'
    PENDING = 'P'
    NONE = 'N'
    FRIENDSHIP_STATUS = (
        (FRIENDS, 'Friends'),
        (PENDING, 'Pending'),
        (NONE, 'None')
    )

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to=_user_profile_directory_path, max_length=255,
                                        null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    friends = models.ManyToManyField('CustomUser')

    pending_routes = models.ManyToManyField('routes.Route', related_name='pending_routes')
    performed_routes = models.ManyToManyField('routes.Route', related_name='performed_routes')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def get_profile_pic(self):
        if self.profile_picture:
            return self.profile_picture.url

        return static('img/non_user.png')

    def get_full_name(self):
        return '{} {}'.format(self.name, self.last_name)

    def get_short_name(self):
        return self.name

    def if_staff(self):
        return self.is_staff

    @property
    def confirm_password(self):
        return ''

    def get_friends_count(self):
        q = CustomUser.objects.get(pk=self.id).friends.all().values_list('id', flat=True)
        return CustomUser.objects.filter(friends=self.id, id__in=q).count()

    def get_pending_requests_count(self):
        q = self.friends.all().values_list('pk', flat=True)
        return CustomUser.objects.filter(friends=self.id).exclude(id__in=q).count()

    def get_friendship_status(self, id):
        if CustomUser.objects.get(pk=id).friends.filter(pk=self.pk).exists():
            if self.friends.filter(pk=id).exists():
                return self.FRIENDS
            return self.PENDING
        return self.NONE

    def get_pending_requests(self):
        q = self.friends.all().values_list('pk', flat=True)
        return CustomUser.objects.filter(friends=self.id).exclude(id__in=q)

    def get_friends(self):
        q = CustomUser.objects.get(pk=self.id).friends.all().values_list('id', flat=True)
        return CustomUser.objects.filter(friends=self.id, id__in=q)

    def get_friends_id(self):
        q = CustomUser.objects.get(pk=self.id).friends.all().values_list('id', flat=True)
        return CustomUser.objects.filter(friends=self.id, id__in=q).values_list('id', flat=True)

    def pending_routes_count(self):
        return self.pending_routes.count()

    def performed_routes_count(self):
        return self.performed_routes.count()

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)


class ConfirmationToken(models.Model):
    token = models.CharField(max_length=36, blank=True, unique=True,
                             default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField('CustomUser')
    expire_date = models.DateTimeField(default=_now_plus_7)

    def is_active(self):
        return datetime.now() < self.expire_date


class UserActivity(models.Model):
    ROUTE = 'RT'
    POINT = 'PT'
    TARGETS = (
        (ROUTE, 'a rota'),
        (POINT, 'o ponto')
    )

    COMMENT = 'CO'
    ACTIONS = (
        (COMMENT, 'comentou'),
    )

    action = models.CharField(max_length=2, choices=ACTIONS)
    target = models.CharField(max_length=2, choices=TARGETS)
    description = models.TextField()
    user = models.ForeignKey('CustomUser')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    ##Related##
    route_comment = models.ForeignKey('routes.RouteComment', null=True)
    point_comment = models.ForeignKey('routes.PointComment', null=True)

    def action_name(self):
        dic = dict(UserActivity.ACTIONS)
        return dic[self.action]

    def target_name(self):
        dic = dict(UserActivity.TARGETS)
        return dic[self.target]

    def user_photo(self):
        return self.user.get_profile_pic()

    def user_name(self):
        return self.user.get_full_name()

    def target_link(self):
        if self.route_comment != None:
            return {'value':'routeDetail','keys':{'id':self.route_comment.route.id}}
        if self.point_comment != None:
            return {'value':'routePointDetail','keys':{'id':self.point_comment.point.id}}

        return None

    def target_object_name(self):
        if self.route_comment != None:
            return self.route_comment.route.title
        if self.point_comment != None:
            return self.point_comment.point.title

        return None

