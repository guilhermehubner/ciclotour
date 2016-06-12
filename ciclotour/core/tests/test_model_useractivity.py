from ciclotour.core.models import CustomUser, UserActivity
from ciclotour.routes.models import FieldKind, Route, RouteComment
from django.test import TestCase


class UserActivityTest(TestCase):
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

        self.routeComment = UserActivity.objects.create(
            action=UserActivity.COMMENT,
            target=UserActivity.ROUTE,
            description='Nice route!! I really pretend to trace it!',
            user=self.user,
            route_comment=self.routeComment
        )

    def test_create(self):
         """Must exist one UserActivity on database"""
         self.assertTrue(UserActivity.objects.exists())

    def test_delete(self):
        """When delete related, UserActivity must be deleted too"""
        self.routeComment.delete()
        self.assertFalse(UserActivity.objects.exists())
