from django.test import TestCase
from ciclotour.routes.models import FieldKind

class FieldKindModelTest(TestCase):
    def setUp(self):
        self.field = FieldKind.objects.create(
            kind='mountainous'
        )

    def test_create(self):
        """One route must exist on database"""
        self.assertTrue(FieldKind.objects.exists())
