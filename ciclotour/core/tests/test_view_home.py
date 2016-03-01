from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """GET / deve retornar status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET / deve renderizar o template index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

