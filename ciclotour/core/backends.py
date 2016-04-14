from ciclotour.core.models.custom_user import CustomUser


class CustomUserAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username, is_active=True)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id, is_active=True)
            return user
        except CustomUser.DoesNotExist:
            return None
