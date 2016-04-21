from django.test import TestCase


class RoutesDetailViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/routes/1/')

    def test_get(self):
        self. assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'routes/routes_detail.html')
