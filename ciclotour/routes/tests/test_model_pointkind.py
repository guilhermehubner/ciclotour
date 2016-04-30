from ciclotour.routes.models import PointKind, _pointkind_icon_directory_path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings


class PointKindModel(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
    def setUp(self):
        TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
        icon = SimpleUploadedFile('test.jpg', TINY_GIF)

        self.point_kind = PointKind.objects.create(
            kind='Wonder Nature',
            icon=icon
        )

    def test_create(self):
        """One pointkind must exist on database"""
        self.assertTrue(PointKind.objects.exists())

    def test_user_directory_path(self):
        """Icon image must be saved in correct path"""
        self.assertEqual(_pointkind_icon_directory_path(self.point_kind, 'test.png'),
                         'pointkind/icons/icon_{}.png'.format(self.point_kind.kind))

    def test_kind_unique(self):
        """Kind must be unique"""
        field = PointKind._meta.get_field('kind')
        self.assertTrue(field.unique)
