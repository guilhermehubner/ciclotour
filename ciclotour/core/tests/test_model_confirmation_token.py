from datetime import datetime, timedelta

from ciclotour.core.models import ConfirmationToken, CustomUser
from django.test import TestCase


class ConfirmationTokenModelTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            name='Guilherme',
            last_name='Hübner',
            email='guilherme_hubner@msn.com',
            password='123456'
        )

        self.token = ConfirmationToken.objects.create(user=user)

    def test_create(self):
        """One confirmation token must exist in database"""
        self.assertTrue(ConfirmationToken.objects.exists())

    def test_expire_date(self):
        """Expire date must be set as now plus 7 days"""
        date = datetime.now() + timedelta(days = 7)
        date = date.replace(hour=23, minute=59, second=59, microsecond=0)

        self.assertEqual(self.token.expire_date, date)
