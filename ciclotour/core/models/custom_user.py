from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


def _user_profile_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]
    return 'users_profile/user_{}/profile.{}'.format(instance.email, file_extension)

class CustomUserManager(BaseUserManager):
    def _create_user(self, name, last_name, email, password, is_staff, is_superuser):
        if not email:
            raise ValueError('The given email must be set')
        if not name:
            raise ValueError('The given name must be set')
        if not last_name:
            raise ValueError('The given last name must be set')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            last_name=last_name,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name, last_name, email, password=None):
        return self._create_user(name, last_name, email, password, False, False)

    def create_superuser(self, name, last_name, email, password=None):
        return self._create_user(name, last_name, email, password, True, True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to=_user_profile_directory_path, max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return '{} {}'.format(self.name, self.last_name)

    def get_short_name(self):
        return self.name

    def if_staff(self):
        return self.is_staff

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)
