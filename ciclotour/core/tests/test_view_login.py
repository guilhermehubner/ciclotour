from ciclotour.core.forms import LoginForm
from ciclotour.core.models import CustomUser
from django.shortcuts import resolve_url
from django.test import TestCase


class LoginViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(resolve_url('login'))

    def test_get(self):
        """GET /login/ must return status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET /login/ must render the template login.html"""
        self.assertTemplateUsed(self.response, 'login.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (
            ('<form', 2),
            ('<input', 10),
            ('type="password"', 3),
            ('type="email"', 2),
            ('type="text"', 2),
            ('type="submit"', 2),
            ('type="checkbox"', 1),
            ('<button', 2)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contain csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have LoginForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, LoginForm)

    def test_logged_get(self):
        """GET /login/ with a user logged in must redirect to home"""
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        self.client.login(username='guilherme_hubner@msn.com', password='123')
        response = self.client.get(resolve_url('login'))

        self.assertRedirects(response, resolve_url('home'))


class LoginViewPostValid(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        data = {
            'email': 'guilherme_hubner@msn.com',
            'password': '123'
        }

        self.response = self.client.post(resolve_url('login'), data=data)

    def test_post(self):
        """POST /login/ with valid data should redirect to home"""
        self.assertRedirects(self.response, resolve_url('home'))

    def test_user_logged_in(self):
        """POST /login/ with valid data should login an user"""
        self.assertIn('_auth_user_id', self.client.session)


class LoginViewPostInvalid(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Guilherme',
                                                   'Hübner',
                                                   'guilherme_hubner@msn.com',
                                                   '123')

        data = {
            'email': 'guilherme_hubner@msn.com',
            'password': '1234'
        }

        self.response = self.client.post(resolve_url('login'), data=data)

    def test_post(self):
        """Invalid POST shouldn't redirect"""
        self.assertEqual(self.response.status_code, 200)

    def test_user_logged_in(self):
        """POST /login/ with invalid data shouldn't login an user"""
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_message(self):
        """POST /login/ with invalid data should show a error message"""
        self.assertContains(self.response, LoginForm.error_messages['invalid_login'])


class LoginViewInvalidFieldsTest(TestCase):
    def test_invalid_email(self):
        """In case of invalid e-mail user must be notified"""
        data = {
            'email': 'guilherme_hubner.com',
            'password': '1234'
        }

        response = self.client.post(resolve_url('login'), data=data)
        self.assertContains(response, 'Insira um endereço de email válido.')

    def test_empty_email(self):
        """In case of empty e-mail user must be notified"""
        data = {
            'email': '',
            'password': '1234'
        }

        response = self.client.post(resolve_url('login'), data=data)
        self.assertContains(response, 'Este campo é obrigatório')

    def test_empty_password(self):
        """In case of empty password user must be notified"""
        data = {
            'email': 'guilherme_hubner@msn.com',
            'password': ''
        }

        response = self.client.post(resolve_url('login'), data=data)
        self.assertContains(response, 'Este campo é obrigatório')
