from ciclotour.core.models import CustomUser
from ciclotour.routes.models import WayPoint, Route, FieldKind
from django.test import TestCase


class WayPointModelTest(TestCase):
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

        self.wayPoint = WayPoint.objects.create(
            kind='I',
            latitude='-19.92171275',
            longitude='-43.93655777',
            route = self.route
        )

    def test_create(self):
        """One waypoint must exist on database"""
        self.assertTrue(WayPoint.objects.exists())
