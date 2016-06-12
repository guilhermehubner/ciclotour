from ciclotour.core.models import CustomUser
from ciclotour.routes.models import FieldKind, Route, RouteComment
from django.test import TestCase


class RouteCommentModelTest(TestCase):
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

        self.routeComment = RouteComment.objects.create(
            description='Nice route!! I really pretend to trace it!',
            route=self.route,
            user=self.user
        )

    def test_create(self):
         """Must exist one RouteComment on database"""
         self.assertTrue(RouteComment.objects.exists())
