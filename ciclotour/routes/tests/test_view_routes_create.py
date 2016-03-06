from django.test import TestCase
from django.shortcuts import resolve_url


class RouteCreateViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(resolve_url('routes:create'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'routes/routes_form.html')
