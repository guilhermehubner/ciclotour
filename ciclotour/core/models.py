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
    date = datetime.now() + timedelta(days = 7)
    return date.replace(hour=23, minute=59, second=59, microsecond=0)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to=_user_profile_directory_path, max_length=255,
                                        null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

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

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)


class ConfirmationToken(models.Model):
    token = models.CharField(max_length=36, blank=True, unique=True,
                             default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField('CustomUser')
    expire_date = models.DateTimeField(default=_now_plus_7)


    def is_active(self):
        return datetime.now() < self.expire_date
