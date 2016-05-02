from ciclotour.core.models import CustomUser
from ciclotour.routes.models import FieldKind, Route, RoutePicture, _route_picture_directory_path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings


class TestModelRoutePicture(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
    def setUp(self):
        TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
        image = SimpleUploadedFile('test.jpg', TINY_GIF)

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

        self.route_picture = RoutePicture.objects.create(
            route=self.route,
            owner=self.user,
            image=image,
            description='A picture of some place in serra do cipó'
        )

    def test_create(self):
        """Must exist one RoutePicture on database"""
        self.assertTrue(RoutePicture.objects.exists())

    def test_user_directory_path(self):
        """RoutePicture image must be saved in correct path"""
        self.assertEqual(_route_picture_directory_path(self.route_picture, 'test.png'),
                         'routes/{}/pictures/routePic.png'.format(self.route_picture.route.pk))
