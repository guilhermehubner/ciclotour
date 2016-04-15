from ciclotour.core.models.custom_user import CustomUser
from django.test import TestCase
from django.shortcuts import resolve_url


class HomeTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        self.client.login(username='guilherme_hubner@msn.com', password='123')

        self.response = self.client.get(resolve_url('home'))

    def test_get(self):
        """GET / must return status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET / must render the template index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_routes_create_link(self):
        """GET / must have a link to create route"""
        self.assertContains(self.response, resolve_url('routes:create'))

    def test_login_required(self):
        """GET / without logged user should redirect to login"""
        self.client.logout()
        response = self.client.get(resolve_url('home'))

        self.assertRedirects(response, resolve_url('login')+'?next=/')

    def test_logout_link(self):
        """GET / must have a link to logout"""
        self.assertContains(self.response, resolve_url('logout'))

