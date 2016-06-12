from ciclotour.core.models import CustomUser
from ciclotour.routes.models import FieldKind, Route, Point, PointKind, PointComment
from django.test import TestCase


class RouteCommentModelTest(TestCase):
    fixtures = ['initial_pointkinds_data.json']

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

        self.point = Point.objects.create(
            title='Cachoeira Andorinhas',
            description='Paisagem maravilhosa!',
            kind=PointKind.objects.all()[0],
            address='Alto Jequitibá - MG',
            latitude=-13.331723,
            longitude=-41.1167099,
            route=self.route
        )

        self.routeComment = PointComment.objects.create(
            description='Nice route!! I really pretend to trace it!',
            point=self.point,
            user=self.user
        )

    def test_create(self):
         """Must exist one PointComment on database"""
         self.assertTrue(PointComment.objects.exists())
