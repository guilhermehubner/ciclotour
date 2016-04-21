from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, name, last_name, email, password, is_staff, is_superuser, is_active=True):
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
            is_active=is_active,
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

    def create_regularuser(self, name, last_name, email, password=None):
        return self._create_user(name, last_name, email, password, False, False, False)