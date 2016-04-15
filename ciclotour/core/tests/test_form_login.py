from ciclotour.core.forms import LoginForm
from ciclotour.core.models.custom_user import CustomUser
from django.test import TestCase


class LoginFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have email and password fields"""
        form = LoginForm()
        expected = ['email', 'password']
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
