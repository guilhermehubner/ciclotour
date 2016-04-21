from ciclotour.core.models import CustomUser
from django.test import TestCase
from ciclotour.routes.models import Route, FieldKind


class RouteModelTest(TestCase):
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

    def test_create(self):
        """One route must exist on database"""
        self.assertTrue(Route.objects.exists())

    def test_has_many_waypoints(self):
        """Route has many waypoints"""
        self.route.waypoint_set.create(
            kind='I',
            latitude='-19.92171275',
            longitude='-43.93655777',
        )

        self.assertEqual(self.route.waypoint_set.count(), 1)
