from ciclotour.core.models import CustomUser
from ciclotour.routes.forms import RouteForm
from django.test import TestCase
from django.shortcuts import resolve_url


class RouteCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        self.client.login(username='guilherme_hubner@msn.com', password='123')

        self.response = self.client.get(resolve_url('routes:create'))

    def test_get(self):
        """GET /routes/create/ must return status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET /routes/create/ must render the template routes/routes_form.html"""
        self.assertTemplateUsed(self.response, 'routes/routes_form.html')

    def test_login_required(self):
        """GET /routes/create/ without logged user should redirect to login"""
        self.client.logout()
        response = self.client.get(resolve_url('routes:create'))

        self.assertRedirects(response, resolve_url('login')+'?next=/routes/create/')

    def test_logout_link(self):
        """GET /routes/create/ must have a link to logout"""
        self.assertContains(self.response, resolve_url('logout'))

    def test_context_has_form(self):
        """Context must have RouteForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, RouteForm)
