from ciclotour.core.models import CustomUser
from ciclotour.routes.models import Route, FieldKind, Polyline
from django.test import TestCase


class PolylineModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_regularuser(
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

        self.polyline = Polyline.objects.create(
            route = self.route,
            encoded_polyline='a'
        )

    def test_create(self):
        """One polyline must exist on database"""
        self.assertTrue(Polyline.objects.exists())
