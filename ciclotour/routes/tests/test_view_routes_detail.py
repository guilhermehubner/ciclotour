from ciclotour.core.models import CustomUser
from ciclotour.routes.models import Route, FieldKind
from django.shortcuts import resolve_url
from django.test import TestCase


class RoutesDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            'Guilherme',
            'Hübner',
            'guilherme_hubner@msn.com',
            '123'
        )

        self.fieldKind = FieldKind.objects.create(
            kind='mountainous'
        )

        self.route = Route.objects.create(
            title='route',
            origin='belo horizonte',
            description='A new route between belo horizonte and serra do cipo',
            owner=self.user,
            field=self.fieldKind
        )

        self.client.login(username='guilherme_hubner@msn.com', password='123')

        self.response = self.client.get(resolve_url('routes:detail', pk=self.route.pk))

    def test_get(self):
        """GET /routes/1/ must return status_code 200"""
        self. assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET /routes/1/ must use template routes/routes_detail.html"""
        self.assertTemplateUsed(self.response, 'routes/routes_detail.html')

    def test_login_required(self):
        """GET /routes/1/ without logged user should redirect to login"""
        self.client.logout()
        response = self.client.get(resolve_url('routes:detail', pk=self.route.pk))

        self.assertRedirects(response, resolve_url('login')+'?next={}'.format(
            resolve_url('routes:detail', pk=self.route.pk)))

    def test_logout_link(self):
        """GET /routes/1/ must have a link to logout"""
        self.assertContains(self.response, resolve_url('logout'))
