from ciclotour.core.forms import LoginForm
from ciclotour.core.models import CustomUser
from django.test import TestCase


class LoginFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have email and password fields"""
        form = LoginForm()
        expected = ['email', 'password', 'remember_me']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_authentication(self):
        """If valid data has given to form, it should make the user authentication"""
        user = CustomUser.objects.create_user('Guilherme',
                                              'Hübner',
                                              'guilherme_hubner@msn.com',
                                              '123')
        form = LoginForm({'email': 'guilherme_hubner@msn.com',
                          'password': '123'})
        form.is_valid()

        self.assertEqual(form.get_user().id, user.id)

    def test_invalid_login(self):
        """If invalid data has given to form, it should return False in validation"""
        form = LoginForm({'email': 'guilherme_hubner@msn.com',
                          'password': '123'})
        self.assertFalse(form.is_valid())

    def test_inactive_login(self):
        """If inactive user data has given to form, it should return False in validation"""
        user = CustomUser.objects.create_regularuser('Guilherme',
                                                     'Hübner',
                                                     'guilherme_hubner@msn.com',
                                                     '123')

        form = LoginForm({'email': 'guilherme_hubner@msn.com',
                          'password': '123'})
        self.assertFalse(form.is_valid())

    def test_invalid_login_message(self):
        """If invalid data has given to form, it should return a message"""
        form = LoginForm({'email': 'guilherme_hubner@msn.com',
                          'password': '123'})
        form.is_valid()
        self.assertSequenceEqual(form.non_field_errors(),
                                 [LoginForm.error_messages['invalid_login']])

    def test_inactive_login_message(self):
        """If inactive user data has given to form, it should return return a message"""
        user = CustomUser.objects.create_regularuser('Guilherme',
                                                     'Hübner',
                                                     'guilherme_hubner@msn.com',
                                                     '123')

        form = LoginForm({'email': 'guilherme_hubner@msn.com',
                          'password': '123'})
        form.is_valid()

        self.assertSequenceEqual(form.non_field_errors(),
                                 [LoginForm.error_messages['invalid_login']])