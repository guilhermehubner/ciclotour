from ciclotour.core.models import CustomUser
from django.shortcuts import resolve_url
from django.test import TestCase


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        self.client.login(username='guilherme_hubner@msn.com', password='123')

        self.response = self.client.get(resolve_url('logout'))

    def test_get(self):
        """GET /logout/ should logout current logged user"""
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_no_logged_user_get(self):
        """GET /logout/ whitout user logged in should redirect to login"""
        self.assertRedirects(self.response, resolve_url('login'))
